"""General configuration
"""
import typing as t
from pathlib import Path
from dataclasses import dataclass, field
from ._base import ConfigBase
from ...helper.exception import MKCTFAPIException


_CONF_DIR = Path.home() / '.config' / 'mkctf'
_CONF_FILE = _CONF_DIR / 'mkctf.yml'


@dataclass
class _FlagConfig:
    prefix: str = 'CTF{'
    suffix: str = '}'

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            prefix=dct['prefix'],
            suffix=dct['suffix'],
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'prefix': self.prefix,
            'suffix': self.suffix,
        }


@dataclass
class _DockerConfig:
    user: str = ''
    registry: str = ''

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            user=dct['user'],
            registry=dct['registry'],
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'user': self.user,
            'registry': self.registry,
        }


@dataclass
class GeneralConfig(ConfigBase):
    """[summary]"""

    tags: t.List[str] = field(default_factory=list)
    difficulties: t.List[str] = field(default_factory=list)
    flag: _FlagConfig = field(default_factory=_FlagConfig)
    domain: str = ''
    docker: _DockerConfig = field(default_factory=_DockerConfig)
    templates_dir: Path = _CONF_DIR / 'templates'
    monitoring_dir: Path = _CONF_DIR / 'templates'

    @classmethod
    def load(cls, filepath: t.Optional[Path] = None):
        if not filepath:
            filepath = _CONF_FILE
        return super(GeneralConfig, cls).load(filepath)

    @classmethod
    def from_dict(cls, dct):
        try:
            return cls(
                tags=dct['tags'],
                difficulties=dct['difficulties'],
                flag=_FlagConfig.from_dict(dct['flag']),
                domain=dct['domain'],
                docker=_DockerConfig.from_dict(dct['docker']),
            )
        except Exception as exc:
            raise MKCTFAPIException(
                "failed to load concept from dict"
            ) from exc

    def to_dict(self):
        return {
            'tags': self.tags,
            'difficulties': self.difficulties,
            'flag': self.flag.to_dict(),
            'domain': self.domain,
            'docker': self.docker.to_dict(),
        }
