# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from aiohttp import ClientSession, ClientTimeout, BasicAuth
from .helper.log import app_log
from .model.config import GeneralConfiguration
from .model.repository import Repository
from .helper.formatting import format_text

# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    """Provides access to all functionalities programmatically"""

    FLAG_SIZE = 16  # 16 bytes
    EXEC_TIMEOUT = 120  # 2 minutes
    RCODE_MAPPING = {
        None: ('TIMEOUT', 'magenta'),
        0: ('SUCCESS', 'green'),
        2: ('N/A', 'grey'),
        3: ('MANUAL', 'yellow'),
        4: ('NOT-IMPLEMENTED', 'yellow'),
    }
    HEALTHY_RCODES = {0, 2, 3}

    @classmethod
    def rcode2str(cls, code):
        """Convert a return code to a string"""
        status, color = cls.RCODE_MAPPING.get(code, ('FAILURE', 'red'))
        status = f'[{status}]'
        if code is not None:
            status += f'(code={code})'
        return format_text(status, color, ['bold'])

    @classmethod
    def rcode2health_str(cls, code):
        """Convert a return code to a health string"""
        color = 'red'
        status = 'UNHEALTHY'
        if code in cls.HEALTHY_RCODES:
            color = 'green'
            status = 'HEALTHY'
        return format_text(f'[{status}]', color, ['bold'])

    def __init__(self, repo_dir, general_conf_path=None):
        """Coargstructs a new iargstance"""
        self._repo_dir = Path(repo_dir)
        self._general_conf = GeneralConfiguration.load(general_conf_path)
        self._general_conf.validate()
        app_log.debug("repository directory: %s", self._repo_dir)
        self._repo = Repository(self._repo_dir, self._general_conf)

    def __assert_valid_repo(self):
        """Checks if repository is valid"""
        self._repo.conf.validate()

    def init(self):
        """"""
        initialized = True
        if self._repo.conf.validate(throw=False):
            app_log.info("repository already initialized.")
        else:
            app_log.info("initializing mkCTF repository...")
            initialized = self._repo.init()
            if initialized:
                app_log.info("repository successfully initialized.")
            else:
                app_log.error("failed to initialize repository.")
        return {'initialized': initialized, 'conf': self._repo.conf}

    def find(self, slug):
        """"""
        self.__assert_valid_repo()
        challenge = self._repo.find(slug)
        if not challenge:
            return None
        return {'slug': challenge.conf.slug, 'conf': challenge.conf.raw}

    def enum(self, tags=None, categories=None, slug=None):
        """"""
        tags = tags or []
        categories = categories or []
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                yield {
                    'slug': challenge.conf.slug,
                    'conf': challenge.conf.raw,
                    'description': challenge.description,
                }

    def create(self, configuration=None):
        """"""
        self.__assert_valid_repo()
        created = self._repo.create_chall(configuration)
        if created:
            app_log.info("challenge successfully created.")
        return {'created': created}

    def delete(self, slug):
        """"""
        self.__assert_valid_repo()
        deleted = self._repo.delete_chall(slug)
        if deleted:
            app_log.info("challenge %s successfully deleted.", slug)
        else:
            app_log.error("challenge %s deletion failed.", slug)
        return {'deleted': deleted}

    def configure(self, configuration=None, slug=None):
        """Configure a challenge

        Mind specifying 'configuration' if you don't want to spawn a command
        line based wizard.
        """
        self.__assert_valid_repo()
        if slug is None:
            # configure repo
            configured = self._repo.configure(configuration)
            if configured:
                app_log.info("repo successfully configured.")
                app_log.warning(
                    "you might want to run `update-meta` command now."
                )
            else:
                app_log.error("repo configuration failed.")
        else:
            # configure a challenge
            configured = self._repo.configure_chall(slug, configuration)
            if configured:
                app_log.info("challenge successfully configured.")
            else:
                app_log.error("challenge configuration failed.")
        return {'configured': configured}

    def enable(self, slug):
        """Enable a challenge"""
        self.__assert_valid_repo()
        enabled = self._repo.enable_chall(slug)
        if enabled:
            app_log.info("%s successfully enabled.", slug)
        return {'enabled': enabled}

    def disable(self, slug):
        """Disable a challenge"""
        self.__assert_valid_repo()
        disabled = self._repo.disable_chall(slug)
        if disabled:
            app_log.info("%s successfully disabled.", slug)
        return {'disabled': disabled}

    async def push(
        self,
        host,
        port=443,
        tags=None,
        categories=None,
        username='',
        password='',
        no_verify_ssl=False,
    ):
        """Push challenge configuration to a scoreboard"""
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        challenges = []
        for challenge in self._repo.scan(tags, categories):
            challenges.append(challenge.conf.raw)
        url = f'https://{host}:{port}/mkctf-api/push'
        ssl = False if no_verify_ssl else None
        auth = BasicAuth(username, password)
        timeout = ClientTimeout(total=2 * 60)
        async with ClientSession(auth=auth, timeout=timeout) as session:
            async with session.post(
                url, ssl=ssl, json={'challenges': challenges}
            ) as resp:
                if resp.status < 400:
                    app_log.info("push succeeded.")
                    return {'pushed': True}
        app_log.error("push failed.")
        return {'pushed': False}

    def export(
        self,
        export_dir,
        tags=None,
        categories=None,
        slug=None,
        include_disabled=False,
    ):
        """Export challenge public data as an archive to 'export_dir' """
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        export_dir.mkdir(parents=True, exist_ok=True)
        app_log.info("exporting challenges public data to: %s", export_dir)
        if not slug:
            for challenge in self._repo.scan(tags, categories):
                archive_path = challenge.export(export_dir, include_disabled)
                if not archive_path:
                    continue
                yield {
                    'slug': challenge.conf.slug,
                    'archive_path': archive_path,
                }
            return
        challenge = self._repo.find(slug)
        if not challenge:
            app_log.error("challenge not found: %s", challenge.conf.slug)
            return
        archive_path = challenge.export(export_dir, include_disabled)
        if not archive_path:
            return
        yield {'slug': challenge.conf.slug, 'archive_path': archive_path}

    def renew_flag(self, tags=None, categories=None, slug=None, size=None):
        """Renew flag for one challenge or more"""
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(
                    "%s's flag has been renewed.", challenge.conf.slug
                )
                app_log.warning(
                    "you might want to call 'build' then 'deploy' to regenerate the challenge and deploy it."
                )
                yield {
                    'slug': challenge.conf.slug,
                    'flag': challenge.renew_flag(size or MKCTFAPI.FLAG_SIZE),
                }

    def update_meta(self, tags=None, categories=None, slug=None):
        """Update static metadata

        Only static_url might be updated at the moment
        """
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                app_log.info("updating %s meta...", challenge.conf.slug)
                static_url = challenge.update_static_url()
                yield {'slug': challenge.conf.slug, 'static_url': static_url}
            app_log.info("done.")

    async def build(
        self, tags=None, categories=None, slug=None, dev=False, timeout=None
    ):
        """Run build executable"""
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                app_log.info("building %s...", challenge.conf.slug)
                result = await challenge.build(
                    dev, timeout or MKCTFAPI.EXEC_TIMEOUT
                )
                result.update({'slug': challenge.conf.slug})
                yield result

    async def deploy(
        self, tags=None, categories=None, slug=None, dev=False, timeout=None
    ):
        """Run deploy executable"""
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"deploying {challenge.conf.slug}...")
                result = await challenge.deploy(
                    dev, timeout or MKCTFAPI.EXEC_TIMEOUT
                )
                result.update({'slug': challenge.conf.slug})
                yield result

    async def healthcheck(
        self, tags=None, categories=None, slug=None, dev=False, timeout=None
    ):
        """Run healthcheck executable"""
        self.__assert_valid_repo()
        tags = tags or []
        categories = categories or []
        for challenge in self._repo.scan(tags, categories):
            if slug is None or slug == challenge.conf.slug:
                app_log.info("checking %s health...", challenge.conf.slug)
                result = await challenge.healthcheck(
                    dev, timeout or MKCTFAPI.EXEC_TIMEOUT
                )
                result.update({'slug': challenge.conf.slug})
                yield result
