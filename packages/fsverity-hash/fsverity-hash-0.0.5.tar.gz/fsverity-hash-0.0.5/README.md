# fsverity-hash

Python implementation of [fs-verity] hash scheme.

## Installation

```
python -mpip install fsverity-hash
```

## Usage

`FSVerityHash` exposes a [hashlib] like interface
```python
>>> import fsverity_hash
>>> m = fsverity_hash.FSVerityHash()
>>> m.update(b"Nobody inspects the spammish repetition")
>>> m.digest()
b'>\xd6s\xd52<\x9e\x1c`\x82\x0f td\xb0\xb8X\xa9\x0b\xa4\xff\x94\x0b\x12=\xd1kBV\x99\xce\xbe'
>>> m.hexdigest()
'3ed673d5323c9e1c60820f207464b0b858a90ba4ff940b123dd16b425699cebe'
```

the `fsverity digest` command produces the same digest

```
$ echo -n "Nobody inspects the spammish repetition" > file.txt
$ fsverity digest file.txt
sha256:3ed673d5323c9e1c60820f207464b0b858a90ba4ff940b123dd16b425699cebe file.txt
```

The module exposes the same command line interface as `fsverity digest`

```
$ echo -n "Nobody inspects the spammish repetition" > spam.txt
$ fsverity digest spam.txt
sha256:3ed673d5323c9e1c60820f207464b0b858a90ba4ff940b123dd16b425699cebe spam.txt
$ python3 -m fsverity_hash spam.txt
sha256:3ed673d5323c9e1c60820f207464b0b858a90ba4ff940b123dd16b425699cebe spam.txt
$ python3 -m fsverity_hash --help
usage: fsverity_hash.py [-h] [--hash-alg {sha256,sha512}] [--block-size BYTES]
                        [--compact]
                        [FILE ...]

Compute fs-verity hashes

positional arguments:
  FILE                  Input file(s) to process (default: stdin)

optional arguments:
  -h, --help            show this help message and exit
  --hash-alg {sha256,sha512}
                        Merkle tree block hashing algorithm (default: sha256)
  --block-size BYTES    Merkle tree block size in bytes (default: 4096)
  --compact             Omit the hash algorithm name when printing digests
```

## Limitations

- Upto 8 GiB can be hashed. This is an implementation limit, not a limitation of fs-verity hashes in general.
- Salted hashes aren't implemented.
- No automated tests.
- No testing of custom block sizes.
- `FSVerityHash` objects cannot be copied.

## Other implementations
- https://git.kernel.org/pub/scm/fs/fsverity/fsverity-utils.git
  reference libfsverity implementation and `fsverity` command
- https://github.com/rvolgers/fs-verity-rs Rust crate

## Further reading
- https://manpages.debian.org/testing/fsverity/fsverity.1.en.html
- https://www.kernel.org/doc/html/v6.1/filesystems/fsverity.html

[fs-verity]: https://www.kernel.org/doc/html/v6.1/filesystems/fsverity.html#file-digest-computation
[hashlib]: https://docs.python.org/3/library/hashlib.html
