# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from aiohttp import ClientSession, ClientTimeout, BasicAuth
from .exception import MKCTFAPIException
from .helper.log import app_log
from .model.config import GeneralConfiguration
from .model.repository import Repository
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    '''Provides access to all functionalities programmatically
    '''
    DEFAULT_TIMEOUT = 120 # 2 minutes
    DEFAULT_FLAG_SIZE = 16 # 16 bytes

    def __init__(self, repo_dir, general_conf_path=None):
        '''Coargstructs a new iargstance
        '''
        self._repo_dir = Path(repo_dir)
        self._general_conf = GeneralConfiguration.load(general_conf_path)
        self._general_conf.validate()
        app_log.debug(f"repository directory: {self._repo_dir}")
        self._repo = Repository(self._repo_dir, self._general_conf)

    def __assert_valid_repo(self):
        '''Checks if repository is valid
        '''
        self._repo.conf.validate()

    def init(self):
        '''
        '''
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
        '''
        '''
        self.__assert_valid_repo()
        challenge =  self._repo.find(slug)
        if not challenge:
            return None
        return {'slug': challenge.conf.slug, 'conf': challenge.conf.raw}

    def enum(self, tags=[], slug=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                yield {
                    'slug': challenge.conf.slug,
                    'conf': challenge.conf.raw,
                    'description': challenge.description,
                }

    def create(self, configuration=None):
        '''
        '''
        self.__assert_valid_repo()
        created = self._repo.create_chall(configuration)
        if created:
            app_log.info("challenge successfully created.")
        return {'created': created}

    def delete(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        deleted = self._repo.delete_chall(slug)
        if deleted:
            app_log.info(f"challenge {slug} successfully deleted.")
        else:
            app_log.error(f"challenge {slug} deletion failed.")
        return {'deleted': deleted}

    def configure(self, configuration=None, slug=None):
        '''Configure a challenge

        Mind specifying 'configuration' if you don't want to spawn a command
        line based wizard.
        '''
        self.__assert_valid_repo()
        if slug is None:
            # configure repo
            configured = self._repo.configure(configuration)
            if configured:
                app_log.info("repo successfully configured.")
                app_log.warning("you might want to run `update-meta` command now.")
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
        '''Enable a challenge
        '''
        self.__assert_valid_repo()
        enabled = self._repo.enable_chall(slug)
        if enabled:
            app_log.info(f"{slug} successfully enabled.")
        return {'enabled': enabled}

    def disable(self, slug):
        '''Disable a challenge
        '''
        self.__assert_valid_repo()
        disabled = self._repo.disable_chall(slug)
        if disabled:
            app_log.info(f"{slug} successfully disabled.")
        return {'disabled': disabled}

    async def push(self, host, port=443, username='', password='', no_verify_ssl=False):
        '''Push challenge configuration to a scoreboard
        '''
        self.__assert_valid_repo()
        challenges = []
        for challenge in self._repo.scan([]):
                challenges.append(challenge.conf.raw)
        url = f'https://{host}:{port}/mkctf-api/push'
        ssl = False if no_verify_ssl else None
        auth = BasicAuth(username, password)
        timeout = ClientTimeout(total=2*60)
        async with ClientSession(auth=auth, timeout=timeout) as session:
            async with session.post(url, ssl=ssl, json={'challenges': challenges}) as resp:
                if resp.status < 400:
                    app_log.info("push succeeded.")
                    return {'pushed': True}
        app_log.error("push failed.")
        return {'pushed': False}

    def export(self, export_dir, tags=[], slug=None, include_disabled=False):
        '''Export challenge public data as an archive to 'export_dir'
        '''
        self.__assert_valid_repo()
        export_dir.mkdir(parents=True, exist_ok=True)
        app_log.info(f"exporting challenges public data to: {export_dir}")
        if not slug:
            for challenge in self._repo.scan(tags):
                archive_path = challenge.export(export_dir, include_disabled)
                yield {
                    'slug': challenge.conf.slug,
                    'archive_path': archive_path
                }
            return
        challenge = self._repo.find(slug)
        if not challenge:
            app_log.error(f"challenge not found: {challenge.conf.slug}")
            return
        archive_path = challenge.export(export_dir, include_disabled)
        yield {
            'slug': challenge.conf.slug,
            'archive_path': archive_path
        }

    def renew_flag(self, tags=[], slug=None, size=None):
        '''Renew flag for one challenge or more
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"{challenge.conf.slug}'s flag has been renewed.")
                app_log.warning("you might want to call 'build' then 'deploy' to regenerate the challenge and deploy it.")
                yield {
                    'slug': challenge.conf.slug,
                    'flag': challenge.renew_flag(size or MKCTFAPI.DEFAULT_FLAG_SIZE)
                }

    def update_meta(self, tags=[], slug=None):
        '''Update static metadata

        Only static_url might be updated at the moment
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"updating {challenge.conf.slug} meta...")
                static_url = challenge.update_static_url()
                yield {
                    'slug': challenge.conf.slug,
                    'static_url': static_url
                }
            app_log.info("done.")

    async def build(self, tags=[], slug=None, dev=False, timeout=None):
        '''Run build executable
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"building {challenge.conf.slug}...")
                result = await challenge.build(dev, timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.conf.slug})
                yield result

    async def deploy(self, tags=[], slug=None, dev=False, timeout=None):
        '''Run deploy executable
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"deploying {challenge.conf.slug}...")
                result = await challenge.deploy(dev, timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.conf.slug})
                yield result

    async def healthcheck(self, tags=[], slug=None, dev=False, timeout=None):
        '''Run healthcheck executable
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.conf.slug:
                app_log.info(f"checking {challenge.conf.slug} health...")
                result = await challenge.healthcheck(dev, timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.conf.slug})
                yield result
