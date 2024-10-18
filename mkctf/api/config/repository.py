"""Repository configuration
"""

from dataclasses import dataclass, field

from yarl import URL

from ...helper.checksum import sha1_hexdigest
from ...helper.random import randbytes, randhex
from ._base import ConfigBase
from .general import GeneralConfig


@dataclass
class _DirsConfig:
    public: list[str] = field(default_factory=list)
    private: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            public=dct['public'],
            private=dct['private'],
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'public': self.public,
            'private': self.private,
        }


@dataclass
class _StaticConfig:
    salt: bytes = randbytes(16)
    base_url: URL = field(default_factory=URL)

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            salt=bytes.fromhex(dct['salt']),
            base_url=URL(dct['base_url']),
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'salt': self.salt.hex(),
            'base_url': str(self.base_url),
        }


@dataclass
class FileConfig:
    name: str = ''
    exec_: bool = False
    from_: str | None = None

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            name=dct['name'],
            exec_=dct.get('exec', False),
            from_=dct.get('from'),
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'name': self.name,
            'exec': self.exec_,
            'from': self.from_,
        }


@dataclass
class _StandardConfig:
    dirs: _DirsConfig = field(default_factory=_DirsConfig)
    build: FileConfig = field(default_factory=FileConfig)
    deploy: FileConfig = field(default_factory=FileConfig)
    healthcheck: FileConfig = field(default_factory=FileConfig)
    description: FileConfig = field(default_factory=FileConfig)
    files: list[FileConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        dct['build']['exec'] = True
        dct['deploy']['exec'] = True
        dct['healthcheck']['exec'] = True
        return cls(
            dirs=_DirsConfig.from_dict(dct['dirs']),
            build=FileConfig.from_dict(dct['build']),
            deploy=FileConfig.from_dict(dct['deploy']),
            healthcheck=FileConfig.from_dict(dct['healthcheck']),
            description=FileConfig.from_dict(dct['description']),
            files=[FileConfig.from_dict(item) for item in dct['files']],
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'dirs': self.dirs.to_dict(),
            'build': self.build.to_dict(),
            'deploy': self.deploy.to_dict(),
            'healthcheck': self.healthcheck.to_dict(),
            'description': self.description.to_dict(),
            'files': [item.to_dict() for item in self.files],
        }


@dataclass
class _CategoryConfig:
    dirs: _DirsConfig = field(default_factory=_DirsConfig)
    files: list[FileConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            dirs=_DirsConfig.from_dict(dct['dirs']),
            files=[FileConfig.from_dict(item) for item in dct['files']],
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'dirs': self.dirs.to_dict(),
            'files': [item.to_dict() for item in self.files],
        }


def _standard_factory():
    return _StandardConfig(
        dirs=_DirsConfig(public=['public']),
        build=FileConfig(name='build', exec_=True, from_='build.jinja'),
        deploy=FileConfig(name='deploy', exec_=True, from_='deploy.jinja'),
        healthcheck=FileConfig(
            name='healthcheck', exec_=True, from_='healthcheck.jinja'
        ),
        description=FileConfig(
            name='description.md', from_='description.md.jinja'
        ),
        files=[
            FileConfig(name='.gitignore'),
            FileConfig(name='writeup.md', from_='writeup.md.jinja'),
            FileConfig(name='healthcheck.deps', from_='healthcheck.deps'),
        ],
    )


def _categories_factory():
    return {
        'simple': _CategoryConfig(dirs=_DirsConfig(private=['private'])),
        'server': _CategoryConfig(
            dirs=_DirsConfig(private=['server']),
            files=[
                FileConfig(name='server/Dockerfile', from_='Dockerfile.server')
            ],
        ),
        'sandbox': _CategoryConfig(
            dirs=_DirsConfig(private=['server']),
            files=[
                FileConfig(
                    name='server/Dockerfile',
                    from_='Dockerfile.sandbox-server',
                ),
                FileConfig(
                    name='server/Dockerfile.sandbox',
                    from_='Dockerfile.server',
                ),
                FileConfig(name='server/banner', from_='banner'),
                FileConfig(name='server/sshd_config', from_='sshd_config'),
                FileConfig(
                    name='server/sandbox_start.sh',
                    exec_=True,
                    from_='sandbox_start.sh.jinja',
                ),
            ],
        ),
    }


@dataclass
class RepositoryConfig(ConfigBase):
    """[summary]"""

    name: str = 'MKCTF CTF'
    static: _StaticConfig = field(default_factory=_StaticConfig)
    general: GeneralConfig = field(default_factory=GeneralConfig)
    standard: _StandardConfig = field(default_factory=_standard_factory)
    categories_: dict[str, _CategoryConfig] = field(
        default_factory=_categories_factory
    )

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        return cls(
            name=dct['name'],
            static=_StaticConfig.from_dict(dct['static']),
            general=GeneralConfig.from_dict(dct['general']),
            standard=_StandardConfig.from_dict(dct['standard']),
            categories_={
                category: _CategoryConfig.from_dict(category_config)
                for category, category_config in dct['categories'].items()
            },
        )

    def to_dict(self):
        """Build dict from instance"""
        return {
            'name': self.name,
            'static': self.static.to_dict(),
            'general': self.general.to_dict(),
            'standard': self.standard.to_dict(),
            'categories': {
                category: category_config.to_dict()
                for category, category_config in self.categories_.items()
            },
        }

    @property
    def categories(self):
        """Configured challenge categories"""
        return list(self.categories_.keys())

    def directories(
        self, category: str, public_only: bool = False
    ) -> list[str]:
        """List dirs of given category

        List public dirs only when public_only is set to True
        """
        directories_ = []
        directories_.extend(self.standard.dirs.public)
        directories_.extend(self.categories_[category].dirs.public)
        if not public_only:
            directories_.extend(self.standard.dirs.private)
            directories_.extend(self.categories_[category].dirs.private)
        return directories_

    def files(self, category: str) -> list[str]:
        """List files of given category"""
        files_ = [
            self.standard.build,
            self.standard.deploy,
            self.standard.healthcheck,
            self.standard.description,
        ]
        files_.extend(self.standard.files)
        files_.extend(self.categories_[category].files)
        return files_

    def make_rand_flag(self, size: int = 16) -> str:
        """Generate a random flag"""
        return ''.join(
            [
                self.general.flag.prefix,
                randhex(size),
                self.general.flag.suffix,
            ]
        )

    def make_static_url(self, slug: str) -> str:
        """Generate a static url"""
        salted_slug = slug.encode() + self.static.salt
        path = f'/{sha1_hexdigest(salted_slug)}.tar.gz'
        return str(self.static.base_url.with_path(path))
