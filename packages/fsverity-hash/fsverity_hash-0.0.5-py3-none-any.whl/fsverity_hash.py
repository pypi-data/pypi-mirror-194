'''
Compute fs-verity hashes
'''
from __future__ import annotations

import enum
import hashlib
import math
import struct


DEFAULT_ALGORITHM = 'sha256'
DEFAULT_BLOCK_SIZE = 4096
NUL = b'\0'


class FSVerityAlgorithm(enum.IntEnum):
    sha256 = 1
    sha512 = 2

    @classmethod
    def from_name(cls, name: str) -> FSVerityAlgorithm:
        try:
            return cls[name]
        except KeyError:
            raise ValueError(f'Unsupported algorithm {name}')

    @property
    def digest_size(self):
        return self.value * (256 // 8)


class FSVerityBlock:
    def __init__(self, data=b'', *, algorithm=DEFAULT_ALGORITHM, size=DEFAULT_BLOCK_SIZE):
        self.algorithm = FSVerityAlgorithm.from_name(algorithm)
        self.data_size = 0
        self.hash = hashlib.new(self.algorithm.name)
        self.size = size
        self.update(data)

    @staticmethod
    def _check_size(algorithm: FSVerityAlgorithm, size: int) -> int:
        try:
            isize = int(size)
        except TypeError:
            raise TypeError(f'Block size must be an integer, not {type(size)}')

        if not math.log2(isize).is_integer() or isize < 2 * algorithm.digest_size:
            raise ValueError(
                f'Invalid block size {size}, '
                f'must be a power of 2 and >= twice algoritm digest size',
            )
        return isize

    def update(self, data):
        assert (self.data_size + len(data)) <= self.size
        self.hash.update(data)
        self.data_size += len(data)

    def digest(self):
        if self.data_size == 0:
            raise ValueError
        h = self.hash.copy()
        h.update(NUL * (self.size - self.data_size))
        return h.digest()

    def hexdigest(self):
        return self.digest().hex()

    @property
    def digest_size(self):
        return self.hash.digest_size

    @property
    def digests_capacity(self):
        return self.size // self.digest_size


class FSVerityHash:
    _descriptor_struct = struct.Struct('<BBBBIQ64s32s144s')
    name = 'fsverity'
    salt = b''
    version = 1

    def __init__(self, data=b'', *, algorithm=DEFAULT_ALGORITHM, block_size=DEFAULT_BLOCK_SIZE):
        self.algorithm = FSVerityAlgorithm.from_name(algorithm)
        self.block_size = FSVerityBlock._check_size(self.algorithm, block_size)
        self.data_size = 0
        self.hashes = []
        self.update(data)

    def update(self, data):
        remaining = memoryview(data)
        while remaining:
            block_used = self.data_size % self.block_size
            if block_used == 0:
                self._update_hashes(remaining)
            block_free = self.block_size - block_used
            chunk, remaining = remaining[:block_free], remaining[block_free:]
            self.hashes[-1].update(chunk)
            self.data_size += len(chunk)
            block_used += len(chunk)
            assert block_used <= self.block_size
            assert self.data_size <= 8 * 2**30

    def _update_hashes(self, pending_data):
        # These transitions must happen only at a block boundary
        # when there is pending data
        assert self.data_size % self.block_size == 0
        assert pending_data

        if self.data_size == 0:
            assert self.hashes == []
            self.hashes[:] = [
                self._new_block(),
            ]
        elif self.data_size == self.block_size:
            assert len(self.hashes) == 1
            self.hashes[:] = [
                self._new_block(self.hashes[0].digest()),
                self._new_block(),
            ]
        elif self.data_size == self.block_size * self.digests_per_block:
            assert len(self.hashes) == 2
            oldroot, oldleaf = self.hashes
            oldroot.update(oldleaf.digest())
            self.hashes[:] = [
                self._new_block(oldroot.digest()),
                self._new_block(),
                self._new_block(),
            ]
        elif self.data_size == self.block_size * self.digests_per_block**2:
            assert len(self.hashes) == 3
            self.hashes[1].update(self.hashes[2].digest())
            self.hashes[0].update(self.hashes[1].digest())
            self.hashes[:] = [
                self._new_block(self.hashes[0].digest()),
                self._new_block(),
                self._new_block(),
                self._new_block(),
            ]

        elif 0 == self.data_size % (self.block_size * self.digests_per_block**2):
            assert len(self.hashes) >= 4, f'expected >= 4, got {len(self.hashes)}'
            self.hashes[-2].update(self.hashes[-1].digest())
            self.hashes[-3].update(self.hashes[-2].digest())
            self.hashes[-4].update(self.hashes[-3].digest())
            self.hashes[-3:] = [
                self._new_block(),
                self._new_block(),
                self._new_block(),
            ]
        elif 0 == self.data_size % (self.block_size * self.digests_per_block):
            assert len(self.hashes) >= 3, f'expected >= 3, got {len(self.hashes)}'
            self.hashes[-2].update(self.hashes[-1].digest())
            self.hashes[-3].update(self.hashes[-2].digest())
            self.hashes[-2:] = [
                self._new_block(),
                self._new_block(),
            ]

        elif 0 == self.data_size % self.block_size:
            assert len(self.hashes) >= 2, f'expected >= 2, got {len(self.hashes)}'
            self.hashes[-2].update(self.hashes[-1].digest())
            self.hashes[-1:] = [
                self._new_block(),
            ]

    def _new_block(self, data=b''):
        return FSVerityBlock(data, algorithm=self.algorithm.name, size=self.block_size)

    def digest(self):
        descriptor = self._descriptor_struct.pack(
            self.version,
            self.algorithm.value,
            math.ceil(math.log2(self.block_size)),
            len(self.salt),
            0,  # reserved
            self.data_size,
            self._merkle_root_digest(),
            self.salt,
            b'',  # reserved
        )
        return hashlib.new(self.algorithm.name, descriptor).digest()

    def _merkle_root_digest(self):
        if self.data_size == 0:
            assert self.hashes == []
            return NUL * self.algorithm.digest_size

        if self.data_size <= self.block_size:
            assert len(self.hashes) == 1
            root = self.hashes[0]
            return root.digest()

        if self.data_size <= self.block_size * self.digests_per_block:
            assert len(self.hashes) == 2, f'expected 2, got {len(self.hashes)}'
            root, leaf = self.hashes
            root.update(leaf.digest())
            return root.digest()

        if self.data_size <= self.block_size * self.digests_per_block**2:
            assert len(self.hashes) == 3, f'expected 3, got {len(self.hashes)}'
            root, mid, leaf = self.hashes
            mid.update(leaf.digest())
            root.update(mid.digest())
            return root.digest()
        if self.data_size <= self.block_size * self.digests_per_block**3:
            assert len(self.hashes) == 4, f'expected 4, got {len(self.hashes)}'
            root, mid1, mid2, leaf = self.hashes
            mid2.update(leaf.digest())
            mid1.update(mid2.digest())
            root.update(mid1.digest())
            return root.digest()
        raise ValueError(f'{self.data_size} not supported yet')

    def hexdigest(self):
        return self.digest().hex()

    @property
    def digest_size(self):
        return self.algorithm.digest_size

    @property
    def digests_per_block(self):
        return self.block_size // self.digest_size


__all__ = [
    'DEFAULT_ALGORITHM',
    'DEFAULT_BLOCK_SIZE',
    FSVerityAlgorithm.__name__,
    FSVerityBlock.__name__,
    FSVerityHash.__name__,
]


if __name__ == '__main__':
    import argparse
    import io
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--hash-alg', default=DEFAULT_ALGORITHM,
        choices=tuple(e.name for e in FSVerityAlgorithm),
        help='Merkle tree block hashing algorithm (default: %(default)s)',
    )
    parser.add_argument(
        '--block-size', default=DEFAULT_BLOCK_SIZE, metavar='BYTES', type=int,
        help='Merkle tree block size in bytes (default: %(default)s)',
    )
    parser.add_argument(
        '--compact', action='store_true',
        help='Omit the hash algorithm name when printing digests',
    )
    parser.add_argument(
        'files', default=[sys.stdin.buffer], metavar='FILE', nargs='*',
        type=argparse.FileType('rb'),
        help='Input file(s) to process (default: stdin)',
    )
    args = parser.parse_args()

    for file in args.files:
        with file as f:
            file_hash = FSVerityHash(
                algorithm=args.hash_alg,
                block_size=args.block_size,
            )
            while data := f.read(io.DEFAULT_BUFFER_SIZE):
                file_hash.update(data)

            if args.compact:
                line = f'{file_hash.hexdigest()} {file.name}'
            else:
                line = f'{file_hash.algorithm.name}:{file_hash.hexdigest()} {file.name}'
        print(line)
