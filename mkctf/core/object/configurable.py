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
from os import scandir
from pprint import pprint
from core.config import yaml_load, yaml_dump
from core.wrapper import lazy
# =============================================================================
#  CLASSES
# =============================================================================

class Configurable(object):
    """[summary]

    [description]
    """
    def __init__(self, logger, conf_path):
        """[summary]

        Arguments:
            logger {Logger} -- [description]
            conf_path {Path} -- [description]
        """
        super().__init__()
        self.conf_path = conf_path
        self.logger = logger

    def _scandirs(self, root, keep=None):
        """Scans a directory for entries

        Arguments:
            root {Path} -- [description]

        Keyword Arguments:
            keep {function} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        dirs = []

        for de in scandir(str(root)):

            if keep is not None and not keep(de):
                continue

            dirs.append(de)

        return dirs


    @lazy()
    def working_dir(self):
        """[summary]

        Decorators:
            lazy

        Returns:
            [type] -- [description]
        """
        return self.conf_path.parent

    def check_conf_exists(self):
        """Checks if configuration file exists and is valid
        """
        return (self.get_conf() is not None)

    def get_conf(self, key=[]):
        """Returns the configuration or specific values

        Keyword Arguments:
            keys {list} -- [description] (default: {[]})

        Returns:
            any -- [description]
        """
        if isinstance(key, str):
            key = [key]

        if not self.conf_path.is_file():
            self.logger.warning("file not found: {}".format(self.conf_path))
            return None

        conf = yaml_load(self.conf_path)

        if len(key) == 0:
            return conf

        value = conf
        while len(key) > 0:
            keyp = key[0]
            key = key[1:]

            value = value.get(keyp)

            if value is None:
                self.logger.warning("missing key: {}".format(keyp))
                return None

            if len(key) > 0 and not isinstance(value, dict):
                self.logger.warning("missing key: {}".format(key[0]))
                return None

        return value

    def set_conf(self, conf):
        """Sets the conf

        Arguments:
            conf {dict} -- [description]
        """
        yaml_dump(self.conf_path, conf)

    def print_conf(self):
        """Prints configuration
        """
        pprint(self.get_conf())
