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
import os
import os.path as path
from shutil import rmtree
from slugify import slugify
from core.cli import CLI
from core.wrapper import lazy
from core.object.challenge import Challenge
from core.object.configurable import Configurable
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for repository.
##
class Repository(Configurable):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      logger       The logger
    ## @param      glob_conf    The glob conf
    ## @param      working_dir  The working dir
    ##
    def __init__(self, logger, conf_path, glob_conf):
        super().__init__(logger, conf_path)
        self.cli = CLI(logger)
        self.glob_conf = glob_conf
    ##
    ## @brief      { function_description }
    ##
    ## @param      root  The root
    ##
    def __scandirs(self, root):
        dirs = []
        for de in os.scandir(root):
            if de.is_dir() and not de.name.startswith('.'):
                dirs.append(de)
        return dirs
    ##
    ## @brief      { function_description }
    ##
    ## @param      prev_conf  The repo conf
    ##
    def __make_repo_conf(self, prev_conf=None):
        def_name = None
        def_categories = None
        def_directories = None
        def_txt_files = None
        def_bin_files = None
        def_chall_file = None
        def_flag_prefix = None
        def_flag_suffix = None

        if prev_conf is not None:
            def_name = prev_conf.get('name')
            def_categories = prev_conf['categories']
            def_directories = prev_conf['directories']
            def_txt_files = prev_conf['files']['txt']
            def_bin_files = prev_conf['files']['bin']
            def_chall_file = prev_conf['files']['config']['challenge']
            def_flag_prefix = prev_conf['flag']['prefix']
            def_flag_suffix = prev_conf['flag']['suffix']

        name = self.cli.readline("enter repository name:",
                                 default=def_name)
        categories = self.cli.choose_many("select categories:",
                                          def_categories,
                                          default=def_categories)
        directories = self.cli.choose_many("select directories:",
                                           def_directories,
                                           default=def_directories)
        txt_files = self.cli.choose_many("select text files:",
                                         def_txt_files,
                                         default=def_txt_files)
        bin_files = self.cli.choose_many("select binary files:",
                                         def_bin_files,
                                         default=def_bin_files)
        challenge_file = self.cli.readline("enter challenge file:",
                                           default=def_chall_file)
        flag_prefix = self.cli.readline("enter flag prefix:",
                                        default=def_flag_prefix)
        flag_suffix = self.cli.readline("enter flag suffix:",
                                        default=def_flag_suffix)

        return {
            'name': name,
            'categories': categories,
            'directories': directories,
            'files': {
                'txt': txt_files,
                'bin': bin_files,
                'config': {
                    'challenge': challenge_file
                }
            },
            'flag': {
                'prefix': flag_prefix,
                'suffix': flag_suffix
            }
        }
    ##
    ## @brief      Makes a chall conf.
    ##
    def __make_chall_conf(self, prev_conf=None):
        repo_conf = self.get_conf()

        def_name = None
        enable = False
        def_static = None
        def_points = None
        def_category = None
        flag = None
        if prev_conf is not None:
            def_name = prev_conf['name']
            enable = prev_conf['enable']
            def_static = prev_conf['static']
            def_points = prev_conf['points']
            def_category = prev_conf['category']
            flag = prev_conf['flag']

        name = self.cli.readline("enter challenge name:",
                                 default=def_name)

        if flag is None or not self.cli.confirm("do you want to keep the old "
                                                "flag ({})?".format(flag)):
            flag = Challenge.make_flag(repo_conf)

        static = self.cli.confirm("is it a static challenge?")
        points = self.cli.readline("enter number of points:",
                                   default=def_points,
                                   expect_digit=True)
        category = self.cli.choose_one("select a category:",
                                       choices=repo_conf['categories'])
        return {
            'name': name,
            'slug': slugify(name),
            'flag': flag,
            'enable': enable,
            'static': static,
            'points': points,
            'category': category,
            'parameters': {}
        }
    ##
    ## @brief      { function_description }
    ##
    def init(self):
        repo_conf = self.__make_repo_conf(self.glob_conf)

        for category in repo_conf['categories']:
            dir_path = path.join(self.working_dir(), category)
            if not path.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        self.set_conf(repo_conf)
        return True
    ##
    ## @brief      { function_description }
    ##
    def scan(self, category=None):
        wd = self.working_dir()
        repo_conf = self.get_conf()
        for cat in self.__scandirs(wd):
            challenges = []
            for chall in self.__scandirs(cat.path):
                chall_conf_path = path.join(chall.path,
                                            repo_conf['files']['config']['challenge'])
                challenges.append(Challenge(self.logger,
                                            chall_conf_path,
                                            repo_conf))

            if category is None:
                yield (cat.name, challenges)
                continue

            if category == cat:
                yield (cat.name, challenges)
                break
    ##
    ## @brief      { function_description }
    ##
    def configure(self):
        repo_conf = self.__make_repo_conf(self.get_conf())
        self.set_conf(repo_conf)
        return True
    ##
    ## @brief      Creates a chall.
    ##
    def create_chall(self):
        repo_conf = self.get_conf()
        chall_conf = self.__make_chall_conf()
        chall_conf_path = path.join(self.working_dir(),
                                    chall_conf['category'],
                                    chall_conf['slug'],
                                    repo_conf['files']['config']['challenge'])

        chall = Challenge(self.logger, chall_conf_path, repo_conf)

        if not chall.create():
            return False

        chall.set_conf(chall_conf)
        return True
    ##
    ## @brief      { function_description }
    ##
    ## @param      challenge  The challenge
    ##
    def configure_chall(self, category, challenge):
        chall_path = path.join(self.working_dir(), category, challenge)

        if not path.isdir(chall_path):
            return False

        repo_conf = self.get_conf()

        chall_conf_path = path.join(chall_path,
                                    repo_conf['files']['config']['challenge'])

        chall = Challenge(self.logger, chall_conf_path, repo_conf)

        new_chall_conf = self.__make_chall_conf(chall.get_conf())

        chall.set_conf(new_chall_conf)
        return True
    ##
    ## @brief      { function_description }
    ##
    ## @param      challenge  The challenge
    ##
    def delete_chall(self, category, challenge):
        chall_path = path.join(self.working_dir(), category, challenge)

        if not path.isdir(chall_path):
            return False

        if not self.cli.confirm("do you really want to remove {}/{}?".format(
                            category, challenge)):
            return False

        rmtree(chall_path)
        return True



