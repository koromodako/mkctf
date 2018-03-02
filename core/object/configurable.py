# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: configurable.py
#     date: 2018-03-02
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
from pprint import pprint
from core.config import yaml_load, yaml_dump
from core.wrapper import lazy
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for configurable.
##
class Configurable(object):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      logger     The logger
    ## @param      conf_path  The conf path
    ##
    def __init__(self, logger, conf_path):
        super().__init__()
        self.conf_path = conf_path
        self.logger = logger
    ##
    ## @brief      { function_description }
    ##
    ## @param      root  The root
    ##
    def _scandirs(self, root, keep=None):
        dirs = []

        for de in os.scandir(root):

            if keep is not None and not keep(de):
                continue

            dirs.append(de)

        return dirs
    ##
    ## @brief      Returns the working directory
    ##
    @lazy('__working_dir')
    def working_dir(self):
        return path.dirname(self.conf_path)
    ##
    ## @brief      Returns True if configuration exists,
    ##             otherwise returns False
    ##
    def check_conf_exists(self):
        return (self.get_conf() is not None)
    ##
    ## @brief      Returns the configuration or a specific value
    ##
    def get_conf(self, keys=[]):
        if not path.isfile(self.conf_path):
            self.logger.warning("file not found: {}".format(self.conf_path))
            return None

        conf = yaml_load(self.conf_path)

        if len(keys) == 0:
            return conf

        value = conf
        while len(keys) > 0:
            key = keys[0]
            keys = keys[1:]

            value = value.get(key)

            if value is None:
                self.logger.warning("missing key: {}".format(key))
                return None

            if len(keys) > 0 and not isinstance(value, dict):
                self.logger.warning("missing key: {}".format(keys[0]))
                return None

        return value
    ##
    ## @brief      Sets the conf.
    ##
    ## @param      conf  The conf
    ##
    def set_conf(self, conf):
        yaml_dump(self.conf_path, conf)
    ##
    ## @brief      { function_description }
    ##
    def print_conf(self):
        pprint(self.get_conf())

