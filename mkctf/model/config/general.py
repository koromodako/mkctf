# ==============================================================================
# IMPORTS
# ==============================================================================
from pathlib import Path
from mkctf.exception import MKCTFAPIException
from .configuration import Configuration
# ==============================================================================
# CLASSES
# ==============================================================================
class GeneralConfiguration(Configuration):
    '''[summary]
    '''
    TYPE = 'general'
    DEFINITION = {
        'tags': (list,),
        'difficulties': (list,),
        'flag': {
            'prefix': (str,),
            'suffix': (str,),
        },
        'domain': (str,),
        'docker': {
            'user': (str,),
            'registry': (str,),
        }
    }
    LOCATION = Path.home().joinpath('.config', 'mkctf', 'mkctf.yml')
    TEMPLATES_DIR = Path.home().joinpath('.config', 'mkctf', 'templates')
    MONITORING_DIR = Path.home().joinpath('.config', 'mkctf', 'monitoring')

    @classmethod
    def load(cls, path):
        if not path:
            path = GeneralConfiguration.LOCATION
        return super(GeneralConfiguration, cls).load(path)

    @property
    def tags(self):
        return self['tags']

    @property
    def difficulties(self):
        return self['difficulties']

    @property
    def flag_prefix(self):
        return self['flag']['prefix']

    @property
    def flag_suffix(self):
        return self['flag']['suffix']

    @property
    def domain(self):
        return self['domain']

    @property
    def docker_user(self):
        return self['docker']['user']

    @property
    def docker_registry(self):
        return self['docker']['registry']
