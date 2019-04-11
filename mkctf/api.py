# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from slugify import slugify
from mkctf.helper.log import app_log
from mkctf.helper.config import config_load
from mkctf.object.repository import Repository
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    '''Provides access to all functionalities programmatically
    '''
    DEFAULT_TIMEOUT = 120 # 2 minutes
    DEFAULT_FLAG_SIZE = 32 # 32 bytes

    def __init__(self, repo_root, config_path=None):
        '''Coargstructs a new iargstance
        '''
        self._repo_root = Path(repo_root)
        app_log.debug(f"repo_root: {self._repo_root}")

        self._glob_conf_path = config_path or Path.home().joinpath('.config', 'mkctf.yml')
        app_log.debug(f"glob_conf_path: {self._glob_conf_path}")

        self._glob_conf = config_load(self._glob_conf_path)
        app_log.debug(f"glob_conf: {self._glob_conf}")

        self._repo_conf_path = self._repo_root / self._glob_conf['files']['repo_conf']
        app_log.debug(f"repo_conf_path: {self._repo_conf_path}")

        self._repo = Repository(self._repo_conf_path, self._glob_conf)

    def __assert_valid_repo(self):
        '''Checks if repository is valid
        '''
        if not self._repo.get_conf():
            app_log.critical("mkctf repository must be initialized first. Run `mkctf init` first.")
            raise RuntimeError("Uninitialized repository.")

    def init(self):
        '''
        '''
        conf = self._repo.get_conf()
        need_init = conf is None
        if need_init:
            self._repo.init()
            app_log.info("mkctf repository successfully created.")
        else:
            app_log.error("already in a mkctf repository.")
        return {'initialized': need_init, 'conf': conf}

    def find(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        challenge =  self._repo.find_chall(slug)
        if not challenge:
            return None
        return {'slug': challenge.slug, 'conf': challenge.get_conf()}

    def enum(self, tags=[], slug=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self._repo.scan(tags):
            if slug is None or slug == challenge.slug:
                yield {
                    'slug': challenge.slug,
                    'conf': challenge.get_conf(),
                    'description': challenge.description,
                }

    def create(self, configuration=None):
        '''
        '''
        self.__assert_valid_repo()
        conf=None
        if configuration:
            slug = slugify(name)
            conf = {
                'name': name,
                'tags': tags,
                'slug': slug,
                'flag': flag,
                'points': points,
                'enabled': enabled,
                'parameters': parameters,
                'standalone': standalone
            }
        created = self._repo.create_chall(conf)
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
                    'flag': challenge.renew_flag(size or MKCTFAPI.DEFAULT_FLAG_SIZE)
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
