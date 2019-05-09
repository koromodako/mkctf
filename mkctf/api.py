# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
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
    DEFAULT_FLAG_SIZE = 32 # 32 bytes

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
        challenge =  self._repo.find_chall(slug)
        if not challenge:
            return None
        return {'slug': challenge.slug, 'conf': challenge.conf.raw}

    def enum(self, tags=[], slug=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                yield {
                    'slug': challenge.slug,
                    'conf': challenge.conf.raw,
                    'description': challenge.description,
                }

    def create(self, configuration):
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

    def configure(self, configuration, slug=None):
        '''
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
        '''
        '''
        self.__assert_valid_repo()
        enabled = self._repo.enable_chall(slug)
        if enabled:
            app_log.info(f"{slug} successfully enabled.")
        return {'enabled': enabled}

    def disable(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        disabled = self._repo.disable_chall(slug)
        if disabled:
            app_log.info(f"{slug} successfully disabled.")
        return {'disabled': disabled}

    def export(self, export_dir, tags=[], slug=None, include_disabled=False):
        '''
        '''
        self.__assert_valid_repo()
        export_dir.mkdir(parents=True, exist_ok=True)
        app_log.info(f"exporting standalone challenges to: {export_dir}")
        if not slug:
            for challenge in self._repo.scan(tags):
                info = challenge.export(export_dir, include_disabled)
                info.update({'slug': challenge.slug})
                yield info
            return
        challenge = self._repo.find_chall(slug)
        if not challenge:
            app_log.error(f"challenge not found: {challenge.slug}")
            return
        info = challenge.export(export_dir, include_disabled)
        info.update({'slug': challenge.slug})
        yield info

    def renew_flag(self, tags=[], slug=None, size=None):
        '''Renews one or more challenge flags
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                app_log.info(f"{slug}'s flag has been renewed.")
                app_log.warning("you might want to call 'build' then 'deploy' to regenerate the challenge and deploy it.")
                yield {
                    'slug': challenge.slug,
                    'flag': challenge.conf.renew_flag(size or MKCTFAPI.DEFAULT_FLAG_SIZE)
                }

    def update_meta(self, tags=[], slug=None):
        '''Update static URL
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                static_url = challenge.conf.update_static_url()
                app_log.info(f"{challenge.slug} mapped to: {static_url}")
                yield {
                    'slug': challenge.slug,
                    'static_url': static_url
                }

    async def build(self, tags=[], slug=None, timeout=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                app_log.info(f"building {challenge.slug}...")
                result = await challenge.build(timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.slug})
                yield result

    async def deploy(self, tags=[], slug=None, timeout=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                app_log.info(f"deploying {challenge.slug}...")
                result = await challenge.deploy(timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.slug})
                yield result

    async def status(self, tags=[], slug=None, timeout=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                app_log.info(f"checking {challenge.slug}'s status...")
                result = await challenge.status(timeout or MKCTFAPI.DEFAULT_TIMEOUT)
                result.update({'slug': challenge.slug})
                yield result
