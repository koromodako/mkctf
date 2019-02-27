# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from slugify import slugify
from mkctf.helper.log import app_log
from mkctf.helper.config import load_config
from mkctf.object.repository import Repository
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    '''Provides access to all functionalities programmatically
    '''
    DEFAULT_TIMEOUT = 60 # seconds
    DEFAULT_FLAG_SIZE = 32

    def __init__(self, repo_root):
        '''Coargstructs a new iargstance
        '''
        self.repo_root = Path(repo_root)
        app_log.debug(f"repo_root: {self.repo_root}")

        self.glob_conf_path = Path.home().joinpath('.config', 'mkctf.yml')
        app_log.debug(f"glob_conf_path: {self.glob_conf_path}")

        self.glob_conf = load_config(self.glob_conf_path)
        app_log.debug(f"glob_conf: {self.glob_conf}")

        self.repo_conf_path = self.repo_root / self.glob_conf['files']['config']['repository']
        app_log.debug(f"repo_conf_path: {self.repo_conf_path}")

        self.repo = Repository(self.repo_conf_path, self.glob_conf)

    def __assert_valid_repo(self):
        '''Checks if repository is valid
        '''
        if not self.repo.get_conf():
            app_log.critical("mkctf repository must be initialized first. Run `mkctf init` first.")
            raise RuntimeError("Uninitialized repository.")

    def init(self):
        '''
        '''
        conf = self.repo.get_conf()
        need_init = conf is None
        if need_init:
            self.repo.init()
            app_log.info("mkctf repository created.")
        else:
            app_log.error("already a mkctf repository.")
        return {'initialized': need_init, 'conf': conf}

    def enum(self, tags=[], slug=None):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                yield {'slug': challenge.slug, 'conf': challenge.get_conf()}

    def create(self, tags, name, flag, points, parameters={}, enabled=False, standalone=True):
        '''
        '''
        self.__assert_valid_repo()
        slug = slugify(name)
        created = self.repo.create_chall({
            'name': name,
            'tags': tags,
            'slug': slug,
            'flag': flag,
            'points': points,
            'enabled': enabled,
            'parameters': parameters,
            'standalone': standalone
        })
        return {'slug': slug, 'created': created}

    def delete(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        deleted = self.repo.delete_chall(slug)
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
            configured = repo.configure(configuration)
            if configured:
                app_log.info("repo configured.")
            else:
                app_log.error("repo configuration failed.")
        else:
            # configure a challenge
            configured = repo.configure_chall(slug, configuration)
            if configured:
                app_log.info("challenge configured.")
            else:
                app_log.error("challenge configuration failed.")
        return {'configured': configured}

    def enable(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        enabled = self.repo.enable_chall(slug)
        return {'enabled': enabled}

    def disable(self, slug):
        '''
        '''
        self.__assert_valid_repo()
        disabled = self.repo.disable_chall(slug)
        return {'disabled': disabled}

    def export(self, export_dir, tags=[], slug=None, include_disabled=False):
        '''
        '''
        self.__assert_valid_repo()
        export_dir.mkdir(parents=True, exist_ok=True)
        app_log.info(f"exporting standalone challenges to: {export_dir}")
        if not slug:
            for challenge in self.repo.scan(tags):
                info = challenge.export(export_dir, include_disabled)
                info.update({'slug': challenge.slug})
                yield info
            return
        challenge = self.repo.find_chall(slug)
        if not challenge:
            app_log.error(f"challenge not found: {challenge.slug}")
            return
        info = challenge.export(export_dir, include_disabled)
        info.update({'slug': challenge.slug})
        yield info

    def renew_flag(self, tags=[], slug=None, size):
        '''Renews one or more challenge flags
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                yield {
                    'slug': challenge.slug,
                    'flag': challenge.renew_flag(size)
                }

    async def build(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await challenge.build(timeout)
                result.update({'slug': challenge.slug})
                yield result

    async def deploy(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await challenge.deploy(timeout)
                result.update({'slug': challenge.slug})
                yield result

    async def status(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await challenge.status(timeout)
                result.update({'slug': challenge.slug})
                yield result
