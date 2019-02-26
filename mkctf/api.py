'''
file: api.py
date: 2018-03-20
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from slugify import slugify
from argparse import ArgumentParser, Namespace
from traceback import print_exc
from mkctf.helper.log import app_log
from mkctf.helper.config import load_config
from mkctf.command.init import init
from mkctf.command.show import show
from mkctf.command.build import build
from mkctf.command.deploy import deploy
from mkctf.command.status import status
from mkctf.command.create import create
from mkctf.command.delete import delete
from mkctf.command.enable import enable
from mkctf.command.export import export
from mkctf.command.disable import disable
from mkctf.command.configure import configure
from mkctf.command.renew_flag import renew_flag
from mkctf.object.repository import Repository
# =============================================================================
#  CONFIGURATION
# =============================================================================
DEFAULT_SIZE = 32
DEFAULT_TIMEOUT = 60 # seconds
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    '''Provides access to all functionalities programmatically
    '''
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
        '''API wrapper for 'init' command
        '''
        conf = self.repo.get_conf()
        if conf is None:
            self.repo.init()
            app_log.info("mkctf repository created.")
            status = True
        else:
            app_log.error("already a mkctf repository.")
            status = False
        return {'status': status, 'conf': conf}

    def list(self):
        '''API wrapper for 'show' command
        '''
        self.__assert_valid_repo()
        results = {}
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                results[challenge.slug] = challenge.get_conf()
        return results

    def create(self, tags, name, flag, points, parameters={}, enabled=False, standalone=True):
        '''API wrapper for 'create' command
        '''
        self.__assert_valid_repo()
        created = self.repo.create_chall({
            'name': name,
            'tags': tags,
            'slug': slugify(name),
            'flag': flag,
            'points': points,
            'enabled': enabled,
            'parameters': parameters,
            'standalone': standalone
        })
        return {'created': created}

    def delete(self, slug=None):
        '''API wrapper for 'delete' command
        '''
        if self.repo.delete_chall(slug):
            app_log.info(f"challenge {slug} successfully deleted.")
            deleted = True
        else:
            app_log.error(f"challenge {slug} deletion failed.")
            deleted = False
        return {'deleted': deleted}

    def configure(self, configuration, slug=None):
        '''API wrapper for 'configure' command
        '''
        configured = False
        if slug is None:
            # configure repo
            if repo.configure(args.configuration):
                app_log.info("repo configured.")
                configured = True
            else:
                app_log.error("repo configuration failed.")
        else:
            # configure a challenge
            if repo.configure_chall(slug, args.configuration):
                app_log.info("challenge configured.")
                configured = True
            else:
                app_log.error("challenge configuration failed.")
        return {'configured': configured}

    def enable(self, slug):
        '''API wrapper for 'enable' command
        '''
        self.__assert_valid_repo()
        enabled = self.repo.enable_chall(slug)
        return {'enabled': enabled}

    def disable(self, slug):
        '''API wrapper for 'disable' command
        '''
        self.__assert_valid_repo()
        disabled = self.repo.disable_chall(args.slug)
        return {'disabled': disabled}

    def __export_chall(self, export_dir, include_disabled, challenge):
        '''Exports one challenge

        Creates an archive containing all of the challenge "exportable" files.
        '''
        if not challenge.is_standalone:
            app_log.warning(f"challenge ignored (not standalone): {challenge.slug}.")
            return False
        if not include_disabled and not challenge.enabled:
            app_log.warning(f"challenge ignored (disabled): {challenge.slug}.")
            return False
        app_log.info(f"exporting {challenge.slug}...")
        archive_name = f'{challenge.slug}.tgz'
        archive_path = export_dir.joinpath(archive_name)
        with tarfile.open(str(archive_path), 'w:gz') as arch:
            for entry in challenge.exportable():
                arch.add(entry.path, arcname=entry.name)
        checksum_name = f'{archive_name}.sha256'
        checksum_path = export_dir.joinpath(checksum_name)
        archive_hash = hash_file(archive_path)
        checksum_path.write_text(f'{archive_hash}  {archive_name}\n')
        app_log.info("done.")
        return {
            'archive_path': archive_path,
            'checksum_path': checksum_path
        }

    def export(self, export_dir, tags=[], slug=None, include_disabled=False):
        '''API wrapper for 'export' command
        '''
        self.__assert_valid_repo()
        results = []
        export_dir.mkdir(parents=True, exist_ok=True)
        if slug:
            challenge = self.repo.find_chall(slug)
            if not challenge:
                app_log.error(f"challenge not found: {challenge.slug}")
                return False
            results.append(self.__export_chall(export_dir, include_disabled, challenge))
        else:
            for challenge in self.repo.scan(tags):
                results.append(self.__export_chall(export_dir, include_disabled, challenge))
        return results

    def renew_flag(self, tags, slug, size):
        '''Renews one or more challenge flags
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                new_flag = challenge.renew_flag(size)
                yield {
                    'slug': challenge.slug,
                    'tags': challenge.tags,
                    'flag': new_flag
                }

    async def __run(self, coro):
        try:
            (code, stdout, stderr) = await coro
            exception = None
        except Exception as exc:
            code = -1
            stdout = b''
            stderr = b''
            exception = str(exc)
        return {
            'slug': challenge.slug,
            'tags': challenge.tags,
            'code': code,
            'stdout': stdout,
            'stderr': stderr,
            'exception': exception
        }

    async def build(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'build' command
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await self.__run(challenge.build(timeout))
                yield result

    async def deploy(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'deploy' command
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await self.__run(challenge.deploy(timeout))
                yield result

    async def status(self, tags=[], slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'status' command
        '''
        self.__assert_valid_repo()
        for challenge in self.repo.scan(tags):
            if slug is None or slug == challenge.slug:
                result = await self.__run(challenge.status(timeout))
                yield result
