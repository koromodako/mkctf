# ==============================================================================
# IMPORTS
# ==============================================================================
from pathlib import Path
from ruamel.yaml import YAML
from mkctf.helper.log import app_log
# ==============================================================================
# CLASSES
# ==============================================================================
class Configuration:
    '''[summary]
    '''
    def __init__(self, path):
        '''[summary]
        '''
        self._conf = None
        self._path = Path(path)
        self._yaml = YAML(typ='safe')
        self._yaml.default_flow_style = False

    @property
    def raw(self):
        return self._conf

    @property
    def path(self):
        return self._path

    def override(self, conf):
        self._conf = conf

    def load(self):
        '''[summary]
        '''
        if not self._path.is_file():
            app_log.error(f"could not find {self._path}")
            return False
        self._conf = self._yaml.load(self._path)
        return True

    def save(self):
        '''[summary]
        '''
        with self._path.open('w') as fp:
            fp.write("#\n"
                     "# This file was generated using mkCTF utility.\n"
                     "# Do not edit it manually unless you know exactly what you're doing.\n"
                     "# Keep #PEBCAK in mind.\n"
                     "#\n")
            self._yaml.dump(self._conf, fp)
