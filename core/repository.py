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
    ## @param      working_dir  The working dir
    ## @param      conf         The conf
    ## @param      logger       The logger
    ##
    def __init__(self, working_dir, conf, logger):
        super().__init__()
        self.logger = logger
        self.conf_file = conf['files']['config']['repository']
        self.categories = conf['categories']
        self.working_dir = working_dir
    ##
    ## @brief      { function_description }
    ##
    def conf_path(self):
        return path.join(self.working_dir, self.conf_file)
    ##
    ## @brief      { function_description }
    ##
    def exists(self):
        return path.isfile(self.conf_path())
    ##
    ## @brief      { function_description }
    ##
    def init(self):
        for category in self.categories:
            dir_path = path.join(self.working_dir, category)
            if not path.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        yaml_dump(self.conf_path(), {
            "working-dir": self.working_dir
        })
        self.logger.info("mkctf repo created.")
