# =============================================================================
#  IMPORTS
# =============================================================================
from shutil import rmtree
from pathlib import Path
from slugify import slugify
import mkctf.helper.cli as cli
from mkctf.helper.log import app_log
from mkctf.helper.wrapper import lazy
from mkctf.object.challenge import Challenge
from mkctf.object.configurable import Configurable
# =============================================================================
#  CLASSES
# =============================================================================
class Repository(Configurable):
    '''[summary]
    '''
    def __init__(self, conf_path, glob_conf):
        '''[summary]
        '''
        super().__init__(conf_path)
        self.glob_conf = glob_conf

    def __make_repo_conf(self, prev={}, override=None):
        '''[summary]
        '''
        if prev is None:
            prev = {}
        if override:
            conf = prev
            conf.update(override)
        else:
            tags = prev.get('tags')
            difficulties = prev.get('difficulties')
            dirs = prev.get('directories', {})
            pub_dirs = dirs.get('public')
            priv_dirs = dirs.get('private')
            files = prev.get('files', {})
            txt_files = files.get('txt')
            flag = prev.get('flag', {})
            name = cli.readline("enter repository name:", default=prev.get('name'))
            tags = cli.choose_many("select tags:", tags, default=tags)
            difficulties = cli.choose_many("select difficulties:", difficulties, default=difficulties)
            pub_dirs = cli.choose_many("select public directories:", pub_dirs, default=pub_dirs)
            priv_dirs = cli.choose_many("select private directories:", priv_dirs, default=priv_dirs)
            txt_files = cli.choose_many("select text files:", txt_files, default=txt_files)
            chall_file = cli.readline("enter challenge file name:", default=files.get('chall_conf'))
            build_file = cli.readline("enter build file name:", default=files.get('build'))
            deploy_file = cli.readline("enter deploy file name:", default=files.get('deploy'))
            status_file = cli.readline("enter status file name:", default=files.get('status'))
            description_file = cli.readline("enter description file name:", default=files.get('description'))
            flag_prefix = cli.readline("enter flag prefix:", default=flag.get('prefix'))
            flag_suffix = cli.readline("enter flag suffix:", default=flag.get('suffix'))
            conf = {
                'name': name,
                'tags': tags,
                'difficulties': difficulties,
                'directories': {
                    'public': pub_dirs,
                    'private': priv_dirs,
                },
                'files': {
                    'txt': txt_files,
                    'build': build_file,
                    'deploy': deploy_file,
                    'status': status_file,
                    'chall_conf': chall_file,
                    'description': description_file,
                },
                'flag': {
                    'prefix': flag_prefix,
                    'suffix': flag_suffix,
                }
            }
        return conf

    def __make_chall_conf(self, prev={}, override=None):
        '''[summary]
        '''
        repo_conf = self.get_conf()
        if prev is None:
            prev = {}
        if override:
            conf = prev
            conf.update(override)
        else:
            flag = prev.get('flag', Challenge.make_flag(repo_conf))
            name = cli.readline("enter challenge name:", default=prev.get('name'))
            tags = cli.choose_many("select one or more tags:", repo_conf['tags'], default=prev.get('tags'))
            points = cli.readline("enter number of points:", default=prev.get('points'), expect_digit=True)
            enabled = prev.get('enabled', False)
            difficulties = repo_conf['difficulties']
            difficulty = cli.choose_one("how difficult is your challenge?", repo_conf['difficulties'], default=prev.get('difficulty', ))
            parameters = prev.get('parameters', {})
            standalone = cli.confirm("is it a standalone challenge?", default=prev.get('standalone'))
            static_url = prev.get('static_url', '')
            company_logo_url = prev.get('company_logo_url', '')
            conf = {
                'name': name,
                'tags': tags,
                'slug': slugify(name),
                'flag': flag,
                'points': points,
                'enabled': enabled,
                'difficulty': difficulty,
                'parameters': parameters,
                'standalone': standalone,
                'static_url': static_url,
                'company_logo_url': company_logo_url
            }
        return conf

    def init(self):
        '''[summary]
        '''
        repo_conf = self.__make_repo_conf(self.glob_conf)
        self.set_conf(repo_conf)
        return True

    def scan(self, tags=[]):
        '''Returns a list of Challenges containing at least one tag in tags

           Notes:
            An empty list of tags means all tags
        '''
        wd = self.working_dir()
        tags = set(tags)
        repo_conf = self.get_conf()
        keep = lambda entry: entry.is_dir() and not entry.name.startswith('.')
        challenges = []
        for chall_dirent in self._scandirs(wd, keep):
            chall_conf_path = Path(chall_dirent.path).joinpath(repo_conf['files']['chall_conf'])
            chall = Challenge(chall_conf_path, repo_conf)
            if not tags or tags.intersection(chall.tags):
                challenges.append(chall)
        return sorted(challenges, key=lambda e: e.slug)

    def find_chall(self, slug):
        '''Finds challenge
        '''
        chall_path = self.working_dir().joinpath(slug)

        if not chall_path.is_dir():
            app_log.warning(f"challenge not found: {slug}")
            return None
        repo_conf = self.get_conf()
        chall_conf_path = chall_path.joinpath(repo_conf['files']['chall_conf'])
        return Challenge(chall_conf_path, repo_conf)

    def configure(self, configuration=None):
        '''Configures repository
        '''
        repo_conf = self.__make_repo_conf(self.get_conf(), override=configuration)
        self.set_conf(repo_conf)
        return True

    def create_chall(self, configuration=None):
        '''Creates a challenge
        '''
        repo_conf = self.get_conf()
        chall_conf = self.__make_chall_conf(override=configuration)
        if not chall_conf['slug']:
            app_log.warning("aborted challenge creation, slug is empty.")
            return False
        chall_conf_path = self.working_dir().joinpath(chall_conf['slug'],
                                                      repo_conf['files']['chall_conf'])
        chall = Challenge(chall_conf_path, repo_conf)
        if not chall.create():
            return False
        chall.set_conf(chall_conf)
        return True

    def configure_chall(self, slug, configuration=None):
        '''Configures a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        new_chall_conf = self.__make_chall_conf(chall.get_conf(), override=configuration)
        chall.set_conf(new_chall_conf)
        return True

    def delete_chall(self, slug):
        '''Deletes a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        if not cli.confirm(f"do you really want to remove {slug}?"):
            app_log.warning("operation cancelled by user.")
            return False
        rmtree(str(chall.working_dir()))
        return True

    def enable_chall(self, slug):
        '''Enables a chalenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        chall.enable(True)
        return True

    def disable_chall(self, slug):
        '''Disables a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False
        chall.enable(False)
        return True
