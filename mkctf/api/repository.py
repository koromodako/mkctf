"""Repository API
"""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree

from ..helper.logging import LOGGER
from ..wizard import ChallengeConfigWizard, RepositoryConfigWizard
from .challenge import ChallengeAPI, create_challenge_api
from .config import ChallengeConfig, GeneralConfig, RepositoryConfig


@dataclass
class RepositoryAPI:
    """Provides programmatic access to repository features"""

    config: RepositoryConfig
    directory: Path
    general_config: GeneralConfig

    @property
    def config_path(self) -> Path:
        """Configuration file path"""
        return self.directory / '.mkctf' / 'repo.yml'

    @property
    def templates_dir(self) -> Path:
        """Templates directory"""
        return self.directory / '.mkctf' / 'templates'

    @property
    def monitoring_dir(self) -> Path:
        """Monitoring directory"""
        return self.directory / '.mkctf' / 'monitoring'

    @property
    def challenges_dir(self) -> Path:
        """Challenges directory"""
        return self.directory / 'challenges'

    @property
    def initialized(self) -> bool:
        """Determine if repository has been initialized"""
        return self.templates_dir.is_dir() and self.config_path.is_file()

    def init(self) -> tuple[bool, str]:
        """[summary]"""
        if self.initialized:
            return False, 'already initialized'
        wizard = RepositoryConfigWizard(general_config=self.general_config)
        config = wizard.show()
        if config is None:
            return False, 'configuration failed'
        self.config = config
        self.directory.mkdir(parents=True, exist_ok=True)
        self.challenges_dir.mkdir(parents=True, exist_ok=True)
        copytree(
            str(self.general_config.templates_dir),
            str(self.templates_dir),
        )
        copytree(
            str(self.general_config.monitoring_dir),
            str(self.monitoring_dir),
        )
        self.config.dump(self.config_path)
        return True, 'initialized'

    def configure(
        self, repo_config_override: RepositoryConfig | None = None
    ) -> bool:
        """Configures repository"""
        final_repo_config = repo_config_override
        if final_repo_config is None:
            wizard = RepositoryConfigWizard(
                general_config=self.general_config,
                existing_config=self.config,
            )
            final_repo_config = wizard.show()
            if final_repo_config is None:
                return False
        self.config = final_repo_config
        self.config.dump(self.config_path)
        return True

    def chall_find(self, slug: str) -> ChallengeAPI | None:
        """Finds challenge"""
        challenge_dir = self.challenges_dir / slug
        if not challenge_dir.is_dir():
            LOGGER.warning("%s not found!", slug)
            return None
        return create_challenge_api(self, challenge_dir)

    def chall_scan(
        self,
        tags: list[str] | set[str] | None = None,
        categories: list[str] | set[str] | None = None,
    ) -> Iterator[ChallengeAPI]:
        """
        Yield challenges having at least one tag in common with tags.
        An empty list of tags means all tags.
        """
        tags = set(tags) or set()
        categories = set(categories) or set()
        for entry in sorted(self.challenges_dir.glob('*')):
            if not entry.is_dir() or entry.name.startswith('.'):
                continue
            challenge_api = create_challenge_api(
                self, self.challenges_dir / entry.name
            )
            if tags and not challenge_api.match_tags(tags):
                LOGGER.debug(
                    "%s does not match selected tags => skipped",
                    challenge_api.config.slug,
                )
                continue
            if categories and not challenge_api.match_categories(categories):
                LOGGER.debug(
                    "%s does not match selected categories => skipped",
                    challenge_api.config.slug,
                )
                continue
            yield challenge_api

    def chall_create(
        self, chall_config_override: ChallengeConfig | None = None
    ) -> bool:
        """Creates a challenge"""
        final_chall_config = chall_config_override
        if final_chall_config is None:
            wizard = ChallengeConfigWizard(repository_config=self.config)
            final_chall_config = wizard.show()
            if final_chall_config is None:
                return False
        challenge_directory = self.challenges_dir / final_chall_config.slug
        if challenge_directory.is_dir():
            LOGGER.error("%s already exists", final_chall_config.slug)
            return False
        challenge_directory.mkdir(parents=True)
        challenge_api = create_challenge_api(self, challenge_directory)
        challenge_api.configure(final_chall_config)
        return challenge_api.init()

    def chall_configure(
        self,
        slug: str,
        chall_config_override: ChallengeConfig | None = None,
    ) -> bool:
        """Configures a challenge"""
        challenge_api = self.chall_find(slug)
        if challenge_api is None:
            return False
        return challenge_api.configure(chall_config_override)

    def chall_delete(self, slug: str) -> bool:
        """Deletes a challenge"""
        challenge_api = self.chall_find(slug)
        if challenge_api is None:
            return False
        return challenge_api.delete()

    def chall_enable(self, slug: str) -> bool:
        """Enables a chalenge"""
        challenge_api = self.chall_find(slug)
        if challenge_api is None:
            return False
        return challenge_api.enable()

    def chall_disable(self, slug: str) -> bool:
        """Disables a challenge"""
        challenge_api = self.chall_find(slug)
        if challenge_api is None:
            return False
        return challenge_api.disable()


def create_repository_api(
    directory: Path, general_config: GeneralConfig
) -> RepositoryAPI:
    """Create RepositoryAPI instance"""
    config = RepositoryConfig.load(directory / '.mkctf' / 'repo.yml')
    return RepositoryAPI(
        config=config,
        directory=directory,
        general_config=general_config,
    )
