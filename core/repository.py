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
from core.config import yaml_load, yaml_dump
from core.challenge import Challenge
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for repository.
##
class Repository(object):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      args         The arguments
    ## @param      logger       The logger
    ## @param      glob_conf    The global conf
    ##
    def __init__(self, args, logger, glob_conf):
        super().__init__()
        self.cli = CLI(logger)
        self.args = args
        self.logger = logger
        self.glob_conf = glob_conf
        self.conf_file = glob_conf['files']['config']['repository']
    ##
    ## @brief      { function_description }
    ##
    def conf_path(self):
        return path.join(self.args.working_dir, self.conf_file)
    ##
    ## @brief      { function_description }
    ##
    def conf(self):
        return yaml_load(self.conf_path())
    ##
    ## @brief      { function_description }
    ##
    def exists(self):
        return path.isfile(self.conf_path())
    ##
    ## @brief      { function_description }
    ##
    def init(self):
        print(self.glob_conf['files'])
        repo_conf = {
            "name": self.cli.read_input("enter repository name: "),
            "categories": self.glob_conf['categories'],
            "directories": self.glob_conf['directories'],
            "files": self.glob_conf['files'],
            "flag": {
                "prefix": self.cli.read_input("enter flag prefix: "),
                "suffix": self.cli.read_input("enter flag suffix: ")
            }
        }

        yaml_dump(self.conf_path(), repo_conf)

        for category in repo_conf['categories']:
            dir_path = path.join(self.args.working_dir, category)
            if not path.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        self.logger.info("mkctf repo created.")
    ##
    ## @brief      { function_description }
    ##
    def configure(self):
        raise NotImplementedError('implement me!')
    ##
    ## @brief      Creates a chall.
    ##
    def create_chall(self):
        repo_conf = self.conf()
        name = self.cli.read_input("enter challenge name: ")
        points = self.cli.read_input("enter number of points: ",
                                     expect_digit=True)
        category = self.cli.choose_one("select a category: ",
                                       among=repo_conf['categories'])
        slug = slugify(name)
        chall_path = path.join(self.args.working_dir, category, slug)

        chall = Challenge(chall_path, repo_conf, self.logger)

        return chall.create(name, points)
    ##
    ## @brief      { function_description }
    ##
    ## @param      challenge  The challenge
    ##
    def configure_chall(self, challenge):
        raise NotImplementedError('implement me!')
    ##
    ## @brief      { function_description }
    ##
    ## @param      challenge  The challenge
    ##
    def delete_chall(self, category, challenge):
        chall_path = path.join(self.args.working_dir, category, challenge)
        if path.isdir(chall_path):
            if self.cli.confirm("do you really want to remove "
                                "{}/{} ?".format(category, challenge)):
                rmtree(chall_path)


