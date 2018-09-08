'''
file: repository.py
date: 2018-02-28
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from shutil import rmtree
from pathlib import Path
from slugify import slugify
from mkctf.helper.cli import CLI
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
        self.cli = CLI()
        self.glob_conf = glob_conf

    def __make_repo_conf(self,
                         previous_conf={},
                         override_conf=None):
        '''[summary]
        '''
        if previous_conf is None:
            previous_conf = {}

        if override_conf:
            conf = previous_conf
            conf.update(override_conf)
        else:
            name = previous_conf.get('name')
            tags = previous_conf.get('tags')
            pub_dirs = previous_conf.get('directories', {}).get('public')
            priv_dirs = previous_conf.get('directories', {}).get('private')
            txt_files = previous_conf.get('files', {}).get('txt')
            chall_file = previous_conf.get('files', {}).get('config', {}).get('challenge')
            build_file = previous_conf.get('files', {}).get('build')
            deploy_file = previous_conf.get('files', {}).get('deploy')
            status_file = previous_conf.get('files', {}).get('status')
            flag_prefix = previous_conf.get('flag', {}).get('prefix')
            flag_suffix = previous_conf.get('flag', {}).get('suffix')

            name = self.cli.readline("enter repository name:", default=name)
            tags = self.cli.choose_many("select tags:", tags, default=tags)
            pub_dirs = self.cli.choose_many("select public directories:", pub_dirs, default=pub_dirs)
            priv_dirs = self.cli.choose_many("select private directories:", priv_dirs, default=priv_dirs)
            txt_files = self.cli.choose_many("select text files:", txt_files, default=txt_files)
            chall_file = self.cli.readline("enter challenge file name:", default=chall_file)
            build_file = self.cli.readline("enter build file name:", default=build_file)
            deploy_file = self.cli.readline("enter deploy file name:", default=deploy_file)
            status_file = self.cli.readline("enter status file name:", default=status_file)
            flag_prefix = self.cli.readline("enter flag prefix:", default=flag_prefix)
            flag_suffix = self.cli.readline("enter flag suffix:", default=flag_suffix)

            conf = {
                'name': name,
                'tags': tags,
                'directories': {
                    'public': pub_dirs,
                    'private': priv_dirs
                },
                'files': {
                    'txt': txt_files,
                    'build': build_file,
                    'deploy': deploy_file,
                    'status': status_file,
                    'config': {
                        'challenge': chall_file
                    }
                },
                'flag': {
                    'prefix': flag_prefix,
                    'suffix': flag_suffix
                }
            }

        return conf

    def __make_chall_conf(self,
                          previous_conf={},
                          override_conf=None):
        '''[summary]
        '''
        repo_conf = self.get_conf()

        if previous_conf is None:
            previous_conf = {}

        if override_conf:
            conf = previous_conf
            conf.update(override_conf)
        else:
            flag = previous_conf.get('flag', Challenge.make_flag(repo_conf))
            enabled = previous_conf.get('enabled', False)
            parameters = previous_conf.get('parameters', {})
            name = previous_conf.get('name')
            tags = previous_conf.get('tags')
            points = previous_conf.get('points')
            standalone = previous_conf.get('standalone')

            name = self.cli.readline("enter challenge name:", default=name)
            tags = self.cli.choose_many("select one or more tags:", repo_conf['tags'], default=tags)
            points = self.cli.readline("enter number of points:", default=points, expect_digit=True)
            standalone = self.cli.confirm("is it a standalone challenge?", default=standalone)

            conf = {
                'name': name,
                'tags': tags,
                'slug': slugify(name),
                'flag': flag,
                'points': points,
                'enabled': enabled,
                'parameters': parameters,
                'standalone': standalone
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

            chall_conf_path = Path(chall_dirent.path).joinpath(repo_conf['files']['config']['challenge'])
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

        chall_conf_path = chall_path.joinpath(repo_conf['files']['config']['challenge'])

        return Challenge(chall_conf_path, repo_conf)

    def configure(self, configuration=None):
        '''Configures repository
        '''
        repo_conf = self.__make_repo_conf(previous_conf=self.get_conf(),
                                          override_conf=configuration)
        self.set_conf(repo_conf)
        return True

    def create_chall(self, configuration=None):
        '''Creates a challenge
        '''
        repo_conf = self.get_conf()
        chall_conf = self.__make_chall_conf(override_conf=configuration)
        chall_conf_path = self.working_dir().joinpath(chall_conf['slug'],
                                                      repo_conf['files']['config']['challenge'])

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

        new_chall_conf = self.__make_chall_conf(previous_conf=chall.get_conf(),
                                                override_conf=configuration)

        chall.set_conf(new_chall_conf)
        return True

    def delete_chall(self, slug):
        '''Deletes a challenge
        '''
        chall = self.find_chall(slug)
        if chall is None:
            return False

        if not self.cli.confirm(f"do you really want to remove {slug}?"):
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
