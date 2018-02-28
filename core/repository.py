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
from core.cli import CLI
from core.config import yaml_dump
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
    def exists(self):
        return path.isfile(self.conf_path())
    ##
    ## @brief      { function_description }
    ##
    def init(self):
        repo_conf = {
            "name": self.cli.read_input("enter repository name: "),
            "categories": self.glob_conf['categories'],
            "directories": self.glob_conf['directories'],
            "files": {
                "txt": self.glob_conf['files']['txt'],
                "bin": self.glob_conf['files']['bin']
            },
            "flag": {
                "prefix": self.cli.read_input("enter flag prefix: "),
                "suffix": self.cli.read_input("enter flag suffix: ")
            }
        }

        yaml_dump(self.conf_path(), repo_conf)

        for category in repo_conf['categories']:
            dir_path = path.join(self.working_dir, category)
            if not path.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        self.logger.info("mkctf repo created.")
