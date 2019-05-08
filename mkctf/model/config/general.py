# ==============================================================================
# IMPORTS
# ==============================================================================
from pathlib import Path
from .configuration import Configuration
# ==============================================================================
# CLASSES
# ==============================================================================
class GeneralConfiguration(Configuration):
    '''[summary]
    '''
    LOCATION = Path.home().joinpath('.config', 'mkctf', 'mkctf.yml')
    TEMPLATES_DIR = Path.home().joinpath('.config', 'mkctf', 'templates')

    def __init__(self):
        '''[summary]
        '''
        if not GeneralConfiguration.LOCATION.is_file():
            raise FileNotFoundError
        super().__init__(GeneralConfiguration.LOCATION)
        self.load()
