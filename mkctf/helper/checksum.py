"""checksum helper
"""

from dataclasses import dataclass, field
from hashlib import sha1, sha256
from pathlib import Path

from .logging import LOGGER


def sha1_hexdigest(data: bytes) -> str:
    """Compute and return data SHA-1 hex digest"""
    return sha1(data).hexdigest()


@dataclass
class ChecksumFile:
    """Represent a checksum file"""

    hashes: list[tuple[str, str]] = field(default_factory=list)

    @property
    def content(self):
        """[summary]"""
        return '\n'.join(
            [
                '\t'.join([hexdigest, filename])
                for hexdigest, filename in self.hashes
            ]
        )

    def add(self, filepath: Path):
        """[summary]"""
        mdigest = sha256()
        LOGGER.debug("computing SHA256 sum of %s", filepath)
        with filepath.open('rb') as fstream:
            while True:
                data = fstream.read(4096)
                if not data:
                    break
                mdigest.update(data)
        self.hashes.append((mdigest.hexdigest(), filepath.name))

    def load(self, filepath: Path):
        """Load hashes from file"""
        for line in filepath.read_text().split('\n'):
            hexdigest, filename = line.split('\t', maxsplit=1)
            self.hashes.append((hexdigest, filename))

    def dump(self, filepath: Path):
        """Dump hashes to file"""
        filepath.write_text(self.content)
