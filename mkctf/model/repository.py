# =============================================================================
#  IMPORTS
# =============================================================================
import shutil
from pathlib import Path
from mkctf.helper.fs import scandir
from mkctf.helper.log import app_log
from mkctf.cli.wizard import *
from mkctf.model.config import (
    GeneralConfiguration,
    RepositoryConfiguration,
)
from .challenge import Challenge
# =============================================================================
#  CLASSES
# =============================================================================
class Repository:
    '''[summary]
    '''
    def __init__(self, repo_dir, general_conf, conf=None):
        '''[summary]
        '''
        self._conf = conf
        self._repo_dir = repo_dir
        self._conf_path = repo_dir.joinpath('.mkctf', 'repo.yml')
        self._general_conf = general_conf
        if not conf:
            self._conf = RepositoryConfiguration.load(self._conf_path)
            if not self._conf.validate(throw=False):
                app_log.warning("repository requires initialization.")

    @property
    def conf(self):
        return self._conf

    @property
    def path(self):
        return self._repo_dir

    @property
    def template_dir(self):
        return self.path.joinpath('.mkctf', 'templates')

    @property
    def challenges_dir(self):
        return self.path.joinpath('challenges')

    @property
    def monitoring_dir(self):
        return self.path.joinpath('monitoring')

    @property
    def initialized(self):
        return self.template_dir.is_dir() and self._conf_path.is_file()

    def _save_conf(self):
        '''Save repository configuration to disk
        '''
        if not self._conf.validate(throw=False):
            app_log.error("save operation aborted: invalid configuration")
            return False
        self._conf.save(self._conf_path)
        return True

    def init(self):
        '''[summary]
        '''
        if not self.initialized:
            wizard = RepositoryConfigurationWizard(self._general_conf)
            if not wizard.show():
                return False
            self._conf = wizard.result
            self.path.mkdir(parents=True, exist_ok=True)
            self.challenges_dir.mkdir(parents=True, exist_ok=True)
            app_log.info("copying templates...")
            shutil.copytree(str(GeneralConfiguration.TEMPLATES_DIR), str(self.template_dir))
            app_log.info("copying monitoring...")
            shutil.copytree(str(GeneralConfiguration.MONITORING_DIR), str(self.monitoring_dir))
            app_log.info("saving repository configuration...")
            return self._save_conf()
        return False

    def scan(self, tags=[], categories=[]):
        '''Returns a list of challenges having at least one tag in common with tags

        An empty list of tags means all tags
        '''
        tags = set(tags)
        categories = set(categories)
        keep = lambda entry: entry.is_dir() and not entry.name.startswith('.')
        challs = []
        for chall_dirent in scandir(self.challenges_dir, keep):
            chall = Challenge(self, self.challenges_dir.joinpath(chall_dirent.name))
            if not chall.conf.validate(throw=False):
                app_log.warning(f"challenge has invalid configuration: {chall.conf.slug} => skipped")
                continue
            if tags and not tags.intersection(chall.conf.tags):
                app_log.warning(f"challenge does not match selected tags: {chall.conf.slug} => skipped")
                continue
            if categories and chall.conf.category not in categories:
                app_log.warning(f"challenge does not match selected categories: {chall.conf.slug} => skipped")
                continue
            challs.append(chall)
        return sorted(challs, key=lambda chall: chall.conf.slug)

    def find(self, slug):
        '''Finds challenge
        '''
        chall_path = self.challenges_dir.joinpath(slug)
        if not chall_path.is_dir():
            app_log.warning(f"challenge not found: {slug}")
            return None
        chall = Challenge(self, chall_path)
        if not chall.conf.validate(throw=False):
            app_log.warning(f"challenge has invalid configuration: {slug}")
            return None
        return chall

    def configure(self, override_conf=None):
        '''Configures repository
        '''
        final_conf = override_conf
        if not final_conf:
            wizard = RepositoryConfigurationWizard(self._general_conf, self.conf)
            if not wizard.show():
                return False
            final_conf = wizard.result
        self._conf = final_conf
        return self._save_conf()

    def create_chall(self, override_conf=None):
        '''Creates a challenge
        '''
        final_conf = override_conf
        if not final_conf:
            wizard = ChallengeConfigurationWizard(self.conf)
            if not wizard.show():
                return False
            final_conf = wizard.result
        chall_path = self.challenges_dir.joinpath(final_conf.slug)
        if chall_path.is_dir():
            app_log.error(f"this challenge ({final_conf.slug}) macthes an existing one")
            return False
        chall = Challenge(self, self.challenges_dir.joinpath(final_conf.slug), final_conf)
        return chall.init()

    def configure_chall(self, slug, override_conf=None):
        '''Configures a challenge
        '''
        chall = self.find(slug)
        if chall is None:
            return False
        return chall.configure(override_conf)

    def delete_chall(self, slug):
        '''Deletes a challenge
        '''
        chall = self.find(slug)
        if chall is None:
            return False
        shutil.rmtree(str(chall.path))
        return True

    def enable_chall(self, slug):
        '''Enables a chalenge
        '''
        chall = self.find(slug)
        if chall is None:
            return False
        chall.enable(True)
        return True

    def disable_chall(self, slug):
        '''Disables a challenge
        '''
        chall = self.find(slug)
        if chall is None:
            return False
        chall.enable(False)
        return True
