"""challenge model
"""

from dataclasses import dataclass, field

from yarl import URL

from ...helper.exception import MKCTFAPIException
from ._base import ConfigBase


@dataclass
class ChallengeConfig(ConfigBase):
    """Challenge concept"""

    name: str = 'MKCTF Challenge'
    slug: str = ''
    tags: list[str] = ''
    flag: str = ''
    author: str = ''
    points: int = -3
    enabled: bool = False
    category: str = ''
    logo_url: URL = field(default_factory=URL)
    difficulty: str = ''
    static_url: URL = field(default_factory=URL)

    @classmethod
    def from_dict(cls, dct):
        try:
            return cls(
                name=dct['name'],
                slug=dct['slug'],
                tags=dct['tags'],
                flag=dct['flag'],
                author=dct['author'],
                points=dct['points'],
                enabled=dct['enabled'],
                category=dct['category'],
                logo_url=URL(dct['logo_url']),
                difficulty=dct['difficulty'],
                static_url=URL(dct['static_url']),
            )
        except Exception as exc:
            raise MKCTFAPIException(
                "failed to create concept from dict"
            ) from exc

    def to_dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'tags': self.tags,
            'flag': self.flag,
            'author': self.author,
            'points': self.points,
            'enabled': self.enabled,
            'category': self.category,
            'logo_url': str(self.logo_url),
            'difficulty': self.difficulty,
            'static_url': str(self.static_url),
        }
