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
    ## @param      prev_conf  The repo conf
    ##
    def __make_repo_conf(self, prev_conf=None):
        if prev_conf is None:
            def_name = None
            def_categories = None
            def_pub_dirs = None
            def_priv_dirs = None
            def_txt_files = None
            def_chall_file = None
            def_build_file = None
            def_deploy_file = None
            def_status_file = None
            def_flag_prefix = None
            def_flag_suffix = None
        else:
            def_name = prev_conf.get('name')
            def_categories = prev_conf['categories']
            def_pub_dirs = prev_conf['directories']['public']
            def_priv_dirs = prev_conf['directories']['private']
            def_txt_files = prev_conf['files']['txt']
            def_chall_file = prev_conf['files']['config']['challenge']
            def_build_file = prev_conf['files']['build']
            def_deploy_file = prev_conf['files']['deploy']
            def_status_file = prev_conf['files']['status']
            def_flag_prefix = prev_conf['flag']['prefix']
            def_flag_suffix = prev_conf['flag']['suffix']


        name = self.cli.readline("enter repository name:",
                                 default=def_name)
        categories = self.cli.choose_many("select categories:",
                                          def_categories,
                                          default=def_categories)
        pub_dirs = self.cli.choose_many("select public directories:",
                                        def_pub_dirs,
                                        default=def_pub_dirs)
        priv_dirs = self.cli.choose_many("select private directories:",
                                         def_priv_dirs,
                                         default=def_priv_dirs)
        txt_files = self.cli.choose_many("select text files:",
                                         def_txt_files,
                                         default=def_txt_files)
        chall_file = self.cli.readline("enter challenge file name:",
                                       default=def_chall_file)
        build_file = self.cli.readline("enter build file name:",
                                       default=def_build_file)
        deploy_file = self.cli.readline("enter deploy file name:",
                                        default=def_deploy_file)
        status_file = self.cli.readline("enter status file name:",
                                        default=def_status_file)
        flag_prefix = self.cli.readline("enter flag prefix:",
                                        default=def_flag_prefix)
        flag_suffix = self.cli.readline("enter flag suffix:",
                                        default=def_flag_suffix)

        return {
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
    ##
    ## @brief      Makes a chall conf.
    ##
    def __make_chall_conf(self, prev_conf=None):
        repo_conf = self.get_conf()

        if prev_conf is None:
            flag = Challenge.make_flag(repo_conf)
            enabled = False
            parameters = {}
            def_name = None
            def_static = None
            def_points = None
            def_category = None
            def_standalone = None
        else:
            flag = prev_conf['flag']
            enabled = prev_conf['enabled']
            parameters = prev_conf['parameters']
            def_name = prev_conf['name']
            def_points = prev_conf['points']
            def_category = prev_conf['category']
            def_standalone = prev_conf['standalone']

        name = self.cli.readline("enter challenge name:",
                                 default=def_name)

        points = self.cli.readline("enter number of points:",
                                   default=def_points,
                                   expect_digit=True)
        category = self.cli.choose_one("select a category:",
                                       choices=repo_conf['categories'],
                                       default=def_category)
        standalone = self.cli.confirm("is it a standalone challenge?",
                                      default=def_standalone)

        return {
            'name': name,
            'slug': slugify(name),
            'flag': flag,
            'points': points,
            'enabled': enabled,
            'category': category,
            'parameters': parameters,
            'standalone': standalone
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
        keep = lambda e: e.is_dir() and not e.name.startswith('.')

        for cat in self._scandirs(wd, keep):
            challenges = []
            for chall in self._scandirs(cat.path, keep):
                chall_conf_path = path.join(chall.path,
                                            repo_conf['files']['config']['challenge'])
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
    ##
    ## @brief      { function_description }
    ##
    ## @param      category  The category
    ## @param      slug      The slug
    ##
    def find_chall(self, category, slug):
        chall_path = path.join(self.working_dir(), category, slug)

        if not path.isdir(chall_path):
            self.logger.warning("challenge not found: "
                                "{}/{}".format(category, slug))
            return None

        repo_conf = self.get_conf()

        chall_conf_path = path.join(chall_path,
                                    repo_conf['files']['config']['challenge'])

        return Challenge(self.logger, chall_conf_path, repo_conf)
    ##
    ## @brief      { function_description }
    ##
    def configure(self, configuration):
        repo_conf = self.__make_repo_conf(previous_conf=self.get_conf(),
                                          override_conf=configuration)
        self.set_conf(repo_conf)
        return True
    ##
    ## @brief      Creates a chall.
    ##
    def create_chall(self, configuration):
        repo_conf = self.get_conf()
        chall_conf = self.__make_chall_conf(override_conf=configuration)
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
    ## @param      category  The category
    ## @param      slug      The slug
    ##
    def configure_chall(self, category, slug, configuration):
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        new_chall_conf = self.__make_chall_conf(previous_conf=chall.get_conf(),
                                                override_conf=configuration)

        chall.set_conf(new_chall_conf)
        return True
    ##
    ## @brief      { function_description }
    ##
    ## @param      category  The category
    ## @param      slug      The slug
    ##
    def delete_chall(self, category, slug):
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        if not self.cli.confirm("do you really want to remove "
                                "{}/{}?".format(category, slug)):
            return False

        rmtree(chall.working_dir())
        return True
    ##
    ## @brief      Enables the chall.
    ##
    ## @param      category  The category
    ## @param      slug      The slug
    ##
    def enable_chall(self, category, slug):
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        chall.enable(True)
        return True
    ##
    ## @brief      Enables the chall.
    ##
    ## @param      category  The category
    ## @param      slug      The slug
    ##
    def disable_chall(self, category, slug):
        chall = self.find_chall(category, slug)
        if chall is None:
            return False

        chall.enable(False)
        return True


