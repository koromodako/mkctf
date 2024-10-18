"""Challenge API
"""

from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree
from stat import S_IRWXU
from tarfile import open as tarfile_open
from tempfile import NamedTemporaryFile

from jinja2 import Template
from yarl import URL

from ..helper.checksum import ChecksumFile
from ..helper.logging import LOGGER
from ..helper.subprocess import CalledProcessResult, run_mkctf_prog
from ..wizard import ChallengeConfigWizard
from .config import ChallengeConfig, FileConfig


@dataclass
class ChallengeAPI:
    """Provides programmatic access to challenge features"""

    config: ChallengeConfig
    directory: Path
    repository_api: 'RepositoryAPI'

    @property
    def repository_config(self):
        """Repository configuration"""
        return self.repository_api.config

    @property
    def config_path(self):
        """Configuration file path"""
        return self.directory / '.mkctf.yml'

    @property
    def description(self) -> str | None:
        """Retrieve challenge description from filesystem"""
        desc_path = (
            self.directory / self.repository_config.standard.description.name
        )
        if not desc_path.is_file():
            return None
        return desc_path.read_text()

    def _create_dir(self, directory: str):
        """Creates a directory"""
        dir_path = self.directory / directory
        if dir_path.is_dir():
            return False
        dir_path.mkdir(parents=True, exist_ok=True)
        return True

    def _create_file(self, file_config: FileConfig):
        """Creates a file"""
        template = file_config.from_
        filepath = self.directory / file_config.name
        filepath.parent.mkdir(parents=True, exist_ok=True)
        content = "# mkCTF generated this file automatically without using a template\n"
        if template:
            tmpl_path = self.repository_api.templates_dir / template
            if tmpl_path.is_file():
                tmpl = Template(tmpl_path.read_text())
                try:
                    content = tmpl.render(
                        challenge_config=self.config,
                        repository_config=self.repository_config,
                    )
                except:
                    content = tmpl_path.read_text()
                    LOGGER.exception(
                        "%s rendering failed, copying template content instead...",
                        filepath,
                    )
        if filepath.is_file():
            return False
        filepath.write_text(content)
        if file_config.exec_:
            filepath.chmod(S_IRWXU)
        return True

    def init(self) -> bool:
        """Create challenge files"""
        self.directory.mkdir(parents=True, exist_ok=True)
        directories_ = self.repository_config.directories(self.config.category)
        for directory in directories_:
            if not self._create_dir(directory):
                LOGGER.warning("directory exists already: %s", directory)
        files_ = self.repository_config.files(self.config.category)
        for file_config in files_:
            if not self._create_file(file_config):
                LOGGER.warning("file exists already: %s", file_config.name)
        self.config.dump(self.config_path)
        return True

    def delete(self) -> bool:
        """Delete challenge"""
        if not self.directory.is_dir():
            LOGGER.warning("challenge does not exist anymore.")
            return False
        rmtree(str(self.directory))
        return True

    def match_slug(self, slug: str) -> bool:
        """Challenge slug matches given slug"""
        return self.config.slug == slug

    def match_tags(self, tags: set[str]) -> bool:
        """Intersection exists between challenge tags and given tags"""
        return bool(tags.intersection(set(self.config.tags)))

    def match_categories(self, categories: set[str]) -> bool:
        """Challenge category matches one of given categories"""
        return self.config.category in categories

    def configure(
        self, chall_config_override: ChallengeConfig | None = None
    ) -> bool:
        """Configure challenge"""
        final_config = chall_config_override
        if not final_config:
            wizard = ChallengeConfigWizard(
                existing_config=self.config,
                repository_config=self.repository_config,
            )
            final_config = wizard.show()
            if final_config is None:
                return False
        self.config = final_config
        self.config.dump(self.config_path)
        return True

    def enable(self) -> bool:
        """Enable the challenge"""
        self.config.enabled = True
        self.config.dump(self.config_path)
        return True

    def disable(self) -> bool:
        """Disable the challenge"""
        self.config.enabled = False
        self.config.dump(self.config_path)
        return True

    def renew_flag(self, size: int) -> str:
        """Replace current flag by a randomly generated one"""
        flag = self.repository_config.make_rand_flag(size)
        self.config.flag = flag
        self.config.dump(self.config_path)
        return flag

    def update_static_url(self) -> URL:
        """Update challenge static url in configuration if required"""
        static_url = self.repository_config.make_static_url(self.config.slug)
        if self.config.static_url != static_url:
            self.config.static_url = static_url
            self.config.dump(self.config_path)
        return static_url

    def export(self, export_directory: Path, export_disabled: bool) -> Path:
        """Export the challenge

        Creates a gzipped tar archive containing all of the challenge "exportable" files
        """
        if not export_disabled and not self.config.enabled:
            LOGGER.warning("export ignored %s (disabled)", self.config.slug)
            return None
        archive_name = self.config.static_url.parts[-1]
        if not archive_name:
            LOGGER.error(
                "export ignored %s (invalid/empty static_url)",
                self.config.slug,
            )
            LOGGER.error(
                "running `mkctf-cli update-meta` should be enough to fix this issue."
            )
            return None
        archive_path = export_directory / archive_name
        checksum_file = ChecksumFile()
        with tarfile_open(str(archive_path), 'w:gz') as arch:
            for directory in self.repository_config.directories(
                self.config.category, public_only=True
            ):
                dir_path = self.directory / directory
                for entry in dir_path.glob('*'):
                    if entry.is_dir():
                        LOGGER.warning(
                            "export ignored %s within %s (directory)",
                            entry,
                            self.config.slug,
                        )
                        continue
                    checksum_file.add(entry)
                    LOGGER.debug("adding %s to archive...", entry)
                    arch.add(str(entry), arcname=entry.name)
            with NamedTemporaryFile('w') as tmpfile:
                tmpfile.write(checksum_file.content)
                tmpfile.flush()
                LOGGER.debug("adding checksum.sha256 to archive...")
                arch.add(tmpfile.name, arcname='checksum.sha256')
        arch_checksum_file = ChecksumFile()
        arch_checksum_file.add(archive_path)
        export_directory.joinpath(f'{archive_name}.sha256').write_text(
            arch_checksum_file.content
        )
        return archive_path

    async def build(
        self, dev: bool = False, timeout: int = 4
    ) -> CalledProcessResult:
        """Build the challenge"""
        return await run_mkctf_prog(
            self.repository_config.standard.build.name,
            self.directory,
            dev,
            timeout,
        )

    async def deploy(
        self, dev: bool = False, timeout: int = 4
    ) -> CalledProcessResult:
        """Deploy the challenge"""
        return await run_mkctf_prog(
            self.repository_config.standard.deploy.name,
            self.directory,
            dev,
            timeout,
        )

    async def healthcheck(
        self, dev: bool = False, timeout: int = 4
    ) -> CalledProcessResult:
        """Check the health of a deployed challenge"""
        return await run_mkctf_prog(
            self.repository_config.standard.healthcheck.name,
            self.directory,
            dev,
            timeout,
        )


def create_challenge_api(
    repository_api: 'RepositoryAPI', directory: Path
) -> ChallengeAPI:
    """Create ChallengeAPI instance"""
    config = ChallengeConfig.load(directory / '.mkctf.yml')
    return ChallengeAPI(
        config=config,
        directory=directory,
        repository_api=repository_api,
    )
