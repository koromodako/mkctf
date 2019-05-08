# =============================================================================
#  IMPORTS
# =============================================================================
import shutil
from pathlib import Path
from mkctf.helper.fs import scandir
from mkctf.helper.log import app_log
from mkctf.helper.cli import Answer, confirm
from .config import GeneralConfiguration, RepositoryConfiguration
from .challenge import Challenge
# =============================================================================
#  CLASSES
# =============================================================================
class Repository:
    '''[summary]
    '''
    def __init__(self, general_conf, repo_dir):
        '''[summary]
        '''
        self._repo_dir = repo_dir
        self._config_file = repo_dir.joinpath('.mkctf', 'repo.yml')
        self._template_dir = repo_dir.joinpath('.mkctf', 'templates')
        self._challenges_dir = repo_dir.joinpath('challenges')
        self._monitoring_dir = repo_dir.joinpath('monitoring')
        self._conf = RepositoryConfiguration(general_conf, self._config_file)

    @property
    def conf(self):
        return self._conf

    @property
    def template_dir(self):
        return self._template_dir

    @property
    def challenges_dir(self):
        return self._challenges_dir

    @property
    def monitoring_dir(self):
        return self._monitoring_dir

    @property
    def initialized(self):
        return self._template_dir.parent.is_dir()

    def init(self):
        '''[summary]
        '''
        self._repo_dir.mkdir(parents=True, exist_ok=True)
        if not self.initialized:
            self._template_dir.parent.mkdir(parents=True)
            shutil.copytree(str(GeneralConfiguration.TEMPLATES_DIR), str(self._template_dir))
            self._conf.update()

    def scan(self, tags=[]):
        '''Returns a list of Challenges containing at least one tag in tags

           Notes:
            An empty list of tags means all tags
        '''
        tags = set(tags)
        keep = lambda entry: entry.is_dir() and not entry.name.startswith('.')
        challenges = []
        for chall_dirent in scandir(self._challenges_dir, keep):
            chall = Challenge(self, Path(chall_dirent.path))
            chall.load()
            if not tags or tags.intersection(chall.conf.tags):
                challenges.append(chall)
        return sorted(challenges, key=lambda challenge: challenge.conf.slug)

    def find_chall(self, slug):
        '''Finds challenge
        '''
        chall_path = self._challenges_dir.joinpath(slug)
        if not chall_path.is_dir():
            app_log.warning(f"challenge not found: {slug}")
            return None
        chall = Challenge(self, chall_path)
        chall.load()
        return chall

    def configure(self, configuration=None):
        '''Configures repository
        '''
        self.conf.update(override_conf=configuration)
        return True

    def create_chall(self, configuration=None):
        '''Creates a challenge
        '''
        return Challenge.create(override_conf=configuration)

    def configure_chall(self, slug, configuration=None):
        '''Configures a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        chall.conf.update(override_conf=configuration)
        return True

    def delete_chall(self, slug):
        '''Deletes a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        if confirm(f"do you really want to remove {slug}") != Answer.YES:
            app_log.warning("operation cancelled by user.")
            return False
        shutil.rmtree(str(chall.path()))
        return True

    def enable_chall(self, slug):
        '''Enables a chalenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        chall.conf.enable(True)
        return True

    def disable_chall(self, slug):
        '''Disables a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        chall.conf.enable(False)
        return True
