"""challenge wizard
"""

from dataclasses import dataclass, field

from slugify import slugify
from yarl import URL

from ..api.config import ChallengeConfig, RepositoryConfig
from ..helper.cli import choose, readline
from ._base import WizardBase


@dataclass
class ChallengeConfigWizard(WizardBase):
    """Challenge configuration wizard"""

    config: ChallengeConfig = field(default_factory=ChallengeConfig)
    existing_config: ChallengeConfig = field(default_factory=ChallengeConfig)
    repository_config: RepositoryConfig = field(
        default_factory=RepositoryConfig
    )

    def _interactive_form(self) -> ChallengeConfig:
        while True:
            # - tags & difficulties
            self.config.name = readline(
                "Enter challenge display name",
                default=self.existing_config.name,
            )
            # consistency: keep previous slug even if challenge renamed
            self.config.slug = self.existing_config.slug or slugify(
                self.config.name
            )
            self.config.tags = choose(
                self.repository_config.general.tags,
                "Tags Selection",
                multi=True,
            )
            tags_str = '\n - '.join(self.config.tags)
            print(f"Selected tags:\n - {tags_str}")
            # consistency: keep previous flag even if challenge renamed
            self.config.flag = (
                self.existing_config.flag
                or self.repository_config.make_rand_flag()
            )
            self.config.author = readline(
                "Enter challenge author name",
                empty=True,
                default=self.existing_config.author,
            )
            self.config.points = readline(
                "Enter challenge points or '-3' for dynamic",
                default=self.existing_config.points,
            )
            # consistency: keep challenge enable state
            self.config.enabled = self.existing_config.enabled
            self.config.category = choose(
                self.repository_config.categories, "Category Selection"
            )
            print(f"Selected category: {self.config.category}")
            self.config.logo_url = URL(
                readline(
                    "Enter challenge logo url",
                    empty=True,
                    default=str(self.existing_config.logo_url),
                )
            )
            self.config.difficulty = choose(
                self.repository_config.general.difficulties,
                "Difficulty Selection",
            )
            print(f"Selected difficulty: {self.config.difficulty}")
            # consistency: keep previous enabled even if challenge renamed
            self.config.static_url = (
                self.existing_config.static_url
                or self.repository_config.make_static_url(self.config.slug)
            )
            return self.config
