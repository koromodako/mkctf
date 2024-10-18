"""repository wizard command
"""

from dataclasses import dataclass, field

from yarl import URL

from ..api.config import GeneralConfig, RepositoryConfig
from ..helper.cli import choose, readline
from ._base import WizardBase


@dataclass
class RepositoryConfigWizard(WizardBase):
    """Repository configuration wizard"""

    general_config: GeneralConfig
    config: RepositoryConfig = field(default_factory=RepositoryConfig)
    existing_config: RepositoryConfig = field(default_factory=RepositoryConfig)

    def _interactive_form(self) -> RepositoryConfig:
        self.config.name = readline(
            "Enter a name", default=self.existing_config.name
        )
        # tags & difficulties
        self.config.general.tags = choose(
            self.general_config.tags,
            "Tags Selection",
            min_count=2,
            multi=True,
            custom=True,
        )
        tags_str = '\n - '.join(self.config.general.tags)
        print(f"Selected tags:\n - {tags_str}")
        self.config.general.difficulties = choose(
            self.general_config.difficulties,
            "Difficulties Selection",
            min_count=2,
            multi=True,
            custom=True,
        )
        difficulties_str = '\n - '.join(self.config.general.difficulties)
        print(f"Selected difficulties:\n - {difficulties_str}")
        # flag
        self.config.general.flag.prefix = readline(
            "Enter flag prefix", default=self.general_config.flag.prefix
        )
        self.config.general.flag.suffix = readline(
            "Enter flag prefix", default=self.general_config.flag.suffix
        )
        # domain
        domain = readline("Enter domain", default=self.general_config.domain)
        self.config.general.domain = domain
        self.config.static.base_url = URL.build(
            scheme='https', host=f'static.{domain}'
        )
        # docker
        self.config.general.docker.user = readline(
            "Enter docker user", default=self.general_config.docker.user
        )
        self.config.general.docker.registry = readline(
            "Enter docker registry host",
            default=self.general_config.docker.registry,
        )
        self.config.standard = self.existing_config.standard
        self.config.categories_ = self.existing_config.categories_
        print(self.config)
        return self.config
