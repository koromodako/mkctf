# =============================================================================
#  IMPORTS
# =============================================================================
from os import scandir
from pprint import pprint
from mkctf.helper.log import app_log
from mkctf.helper.config import config_load, config_dump
from mkctf.helper.wrapper import lazy
# =============================================================================
#  CLASSES
# =============================================================================
class Configurable(object):
    '''[summary]
    '''
    def __init__(self, conf_path):
        '''[summary]
        '''
        super().__init__()
        self.conf_path = conf_path

    def _scandirs(self, root, keep=None):
        '''Scans a directory for entries
        '''
        dirs = []
        for de in scandir(str(root)):
            if keep is not None and not keep(de):
                continue
            dirs.append(de)
        return dirs

    @lazy()
    def working_dir(self):
        '''[summary]
        '''
        return self.conf_path.parent

    def check_conf_exists(self):
        '''Checks if configuration file exists and is valid
        '''
        return (self.get_conf() is not None)

    def get_conf(self, key=[]):
        '''Returns the configuration or specific values
        '''
        if isinstance(key, str):
            key = [key]
        if not self.conf_path.is_file():
            app_log.warning(f"file not found: {self.conf_path}")
            return None
        conf = config_load(self.conf_path)
        if len(key) == 0:
            return conf
        value = conf
        while len(key) > 0:
            keyp = key[0]
            key = key[1:]
            value = value.get(keyp)
            if value is None:
                app_log.warning(f"missing key: {keyp}")
                return None
            if len(key) > 0 and not isinstance(value, dict):
                app_log.warning(f"missing key: {key[0]}")
                return None
        return value

    def set_conf(self, conf):
        '''Sets the conf
        '''
        config_dump(self.conf_path, conf)

    def print_conf(self):
        '''Prints configuration
        '''
        pprint(self.get_conf())
