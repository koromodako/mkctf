# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: repository.py
#     date: 2018-02-28
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from shutil import rmtree
from pathlib import Path
from slugify import slugify
from core.cli import CLI
from core.wrapper import lazy
from core.object.challenge import Challenge
from core.object.configurable import Configurable
# =============================================================================
#  CLASSES
# =============================================================================

class Repository(Configurable):
    """[summary]

    Extends:
        Configurable
    """

    def __init__(self, logger, conf_path, glob_conf):
        """[summary]

        Arguments:
            logger {[type]} -- [description]
            conf_path {[type]} -- [description]
            glob_conf {[type]} -- [description]
        """
        super().__init__(logger, conf_path)
        self.cli = CLI(logger)
        self.glob_conf = glob_conf

    def __make_repo_conf(self,
                         previous_conf={},
                         override_conf=None):
        """[summary]

        Keyword Arguments:
            previous_conf {dict} -- [description] (default: {{}})
            override_conf {dict or None} -- [description] (default: {None})

        Returns:
            dict -- [description]
        """
        if previous_conf is None:
            previous_conf = {}

        if override_conf:
            conf = previous_conf
            conf.update(override_conf)
        else:
            name = previous_conf.get('name')
            categories = previous_conf.get('categories')
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
            categories = self.cli.choose_many("select categories:", categories, default=categories)
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
                'categories': categories,
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
        """[summary]

        Keyword Arguments:
            previous_conf {dict} -- [description] (default: {None})
            override_conf {dict} -- [description] (default: {None})

        Returns:
            dict -- [description]
        """
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
            points = previous_conf.get('points')
            category = previous_conf.get('category')
            standalone = previous_conf.get('standalone')

            name = self.cli.readline("enter challenge name:", default=name)
            points = self.cli.readline("enter number of points:", default=points, expect_digit=True)
            category = self.cli.choose_one("select a category:", choices=repo_conf['categories'], default=category)
            standalone = self.cli.confirm("is it a standalone challenge?", default=standalone)

            conf = {
                'name': name,
                'slug': slugify(name),
                'flag': flag,
                'points': points,
                'enabled': enabled,
                'category': category,
                'parameters': parameters,
                'standalone': standalone
            }

        return conf

    def init(self):
        """[summary]

        [description]

        Returns:
            bool -- [description]
        """
        repo_conf = self.__make_repo_conf(self.glob_conf)

        for category in repo_conf['categories']:
            dir_path = self.working_dir().joinpath(category)
            if not dir_path.is_dir():
                dir_path.mkdir(parents=True, exist_ok=True)

        self.set_conf(repo_conf)
        return True

    def scan(self, category=None):
        """Yields (category, challenges) tuples

        Keyword Arguments:
            category {[type]} -- [description] (default: {None})

        Yields:
            (str, list(Challenge))
        """
        wd = self.working_dir()
        repo_conf = self.get_conf()
        keep = lambda e: e.is_dir() and not e.name.startswith('.')

        for cat in self._scandirs(wd, keep):
            challenges = []
            for chall in self._scandirs(cat.path, keep):
                chall_conf_path = Path(chall.path).joinpath(repo_conf['files']['config']['challenge'])
                challenges.append(Challenge(self.logger,
                                            chall_conf_path,
                                            repo_conf))

            challenges = sorted(challenges, key=lambda e: e.slug())

            if category is None:
                yield (cat.name, challenges)
                continue

            if category == cat.name:
                yield (cat.name, challenges)
                break

    def find_chall(self, category, slug):
        """Finds challenge

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            Challenge -- [description]
        """
        chall_path = self.working_dir().joinpath(category, slug)

        if not chall_path.is_dir():
            self.logger.warning("challenge not found: "
                                "{}/{}".format(category, slug))
            return None

        repo_conf = self.get_conf()

        chall_conf_path = chall_path.joinpath(repo_conf['files']['config']['challenge'])

        return Challenge(self.logger, chall_conf_path, repo_conf)

    def configure(self, configuration=None):
        """Configures repository

        Keyword Arguments:
            configuration {dict or None} -- [description] (default: {None})

        Returns:
            bool -- [description]
        """
        repo_conf = self.__make_repo_conf(previous_conf=self.get_conf(),
                                          override_conf=configuration)
        self.set_conf(repo_conf)
        return True

    def create_chall(self, configuration=None):
        """Creates a challenge

        Keyword Arguments:
            configuration {dict} -- [description] (default: {None})

        Returns:
            bool -- [description]
        """
        repo_conf = self.get_conf()
        chall_conf = self.__make_chall_conf(override_conf=configuration)
        chall_conf_path = self.working_dir().joinpath(chall_conf['category'],
                                                      chall_conf['slug'],
                                                      repo_conf['files']['config']['challenge'])

        chall = Challenge(self.logger, chall_conf_path, repo_conf)

        if not chall.create():
            return False

        chall.set_conf(chall_conf)
        return True

    def configure_chall(self, category, slug, configuration=None):
        """Configures a challenge

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Keyword Arguments:
            configuration {dict} -- [description] (default: {None})

        Returns:
            bool -- [description]
        """
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        new_chall_conf = self.__make_chall_conf(previous_conf=chall.get_conf(),
                                                override_conf=configuration)

        chall.set_conf(new_chall_conf)
        return True

    def delete_chall(self, category, slug):
        """Deletes a challenge

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            bool -- [description]
        """
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        if not self.cli.confirm("do you really want to remove "
                                "{}/{}?".format(category, slug)):
            return False

        rmtree(str(chall.working_dir()))
        return True

    def enable_chall(self, category, slug):
        """Enables a chalenge

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            bool -- [description]
        """
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        chall.enable(True)
        return True

    def disable_chall(self, category, slug):
        """Disables a challenge

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            bool -- [description]
        """
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        chall.enable(False)
        return True
