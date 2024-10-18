"""MKCTF API implementation
"""

from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aiohttp import BasicAuth, ClientSession, ClientTimeout
from yarl import URL

from ..helper.subprocess import CalledProcessResult
from .challenge import ChallengeAPI
from .config import ChallengeConfig, GeneralConfig, RepositoryConfig
from .repository import RepositoryAPI, create_repository_api

FLAG_SIZE = 16  # 16 bytes


@dataclass
class MKCTFAPI:
    """Provides programmatic access to all features"""

    repository_api: RepositoryAPI

    def init(self) -> tuple[bool, str]:
        """Initialize mkctf repository"""
        return self.repository_api.init()

    def find(self, slug: str) -> ChallengeAPI:
        """Find challenge by slug"""
        return self.repository_api.chall_find(slug)

    def enum(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
    ) -> Iterator[ChallengeAPI]:
        """Enumerate challenges"""
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                yield challenge_api

    def create(self, challenge_config: ChallengeConfig | None = None) -> bool:
        """Create a challenge"""
        return self.repository_api.chall_create(challenge_config)

    def delete(self, slug: str) -> bool:
        """Delete a challenge"""
        return self.repository_api.chall_delete(slug)

    def configure(
        self,
        repository_config: RepositoryConfig | None = None,
        slug: str | None = None,
    ) -> bool:
        """Configure a challenge

        Mind specifying 'configuration' if you don't want to spawn a command
        line based wizard.
        """
        if slug is None:
            # configure repo
            return self.repository_api.configure(repository_config)
        # configure a challenge
        return self.repository_api.chall_configure(slug)

    def enable(self, slug: str) -> bool:
        """Enable a challenge"""
        return self.repository_api.chall_enable(slug)

    def disable(self, slug: str) -> bool:
        """Disable a challenge"""
        return self.repository_api.chall_disable(slug)

    def export(
        self,
        export_directory: Path,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
        export_disabled: bool = False,
    ) -> Iterator[tuple[str, Path]]:
        """Export challenge public data as an archive to given export_directory"""
        tags = tags or []
        categories = categories or []
        export_directory.mkdir(parents=True, exist_ok=True)
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                archive_path = challenge_api.export(
                    export_directory, export_disabled
                )
                if not archive_path:
                    continue
                yield challenge_api.config.slug, archive_path

    def renew_flag(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
        size: int | None = None,
    ) -> Iterator[tuple[str, str]]:
        """Renew flag for one challenge or more"""
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                flag = challenge_api.renew_flag(size or FLAG_SIZE)
                yield challenge_api.config.slug, flag

    def update_meta(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
    ) -> Iterator[tuple[str, URL]]:
        """Update static metadata

        Only static_url might be updated at the moment
        """
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                static_url = challenge_api.update_static_url()
                yield challenge_api.config.slug, static_url

    async def push(
        self,
        base_url: URL,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        username: str = '',
        password: str = '',
        no_verify_ssl: bool = False,
    ) -> tuple[bool, str]:
        """Push challenge configuration to a dashboard API"""
        tags = tags or []
        categories = categories or []
        challenges = [
            challenge_api.config.to_dict()
            for challenge_api in self.repository_api.chall_scan(
                tags, categories
            )
        ]
        url = base_url.with_path('/mkctf-api/push')
        ssl = False if no_verify_ssl else None
        auth = BasicAuth(username, password)
        timeout = ClientTimeout(total=2 * 60)
        async with ClientSession(auth=auth, timeout=timeout) as session:
            try:
                async with session.post(
                    url, ssl=ssl, json={'challenges': challenges}
                ) as resp:
                    if resp.status < 400:
                        return True, 'pushed'
                    return False, f'server status: {resp.status}'
            except Exception as exc:
                return False, str(exc)

    async def build(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
        dev: bool = False,
        timeout: int | None = None,
    ) -> tuple[str, CalledProcessResult]:
        """Run build executable"""
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                cpr = await challenge_api.build(dev, timeout)
                yield challenge_api.config.slug, cpr

    async def deploy(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
        dev: bool = False,
        timeout: int | None = None,
    ) -> tuple[str, CalledProcessResult]:
        """Run deploy executable"""
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                cpr = await challenge_api.deploy(dev, timeout)
                yield challenge_api.config.slug, cpr

    async def healthcheck(
        self,
        tags: set[str] | None = None,
        categories: set[str] | None = None,
        slug: str | None = None,
        dev: bool = False,
        timeout: int | None = None,
    ) -> tuple[str, CalledProcessResult]:
        """Run healthcheck executable"""
        tags = tags or []
        categories = categories or []
        for challenge_api in self.repository_api.chall_scan(tags, categories):
            if slug is None or challenge_api.match_slug(slug):
                cpr = await challenge_api.healthcheck(dev, timeout)
                yield challenge_api.config.slug, cpr


def create_mkctf_api(repository_directory: Path) -> MKCTFAPI:
    """Create MKCTFAPI instance"""
    general_config = GeneralConfig.load()
    repository_api = create_repository_api(
        repository_directory, general_config
    )
    return MKCTFAPI(repository_api=repository_api)
