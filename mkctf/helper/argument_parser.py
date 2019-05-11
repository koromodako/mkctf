# ==============================================================================
#  IMPORTS
# ==============================================================================
from pathlib import Path
from argparse import ArgumentParser
from .log import app_log, log_enable_debug, log_enable_logging
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFArgumentParser(ArgumentParser):
    '''A specialised argument parser to define common arguments
    '''
    def __init__(self, *args, **kwargs):
        '''Construct a mkCTF argument parser
        '''
        self._banner = kwargs.get('banner')
        if self._banner:
            del kwargs['banner']
        super().__init__(*args, **kwargs)
        self.add_argument('-q', '--quiet', action='store_true', help="disable logging")
        self.add_argument('-d', '--debug', action='store_true', help="enable debug messages")
        self.add_argument('-r', '--repo-dir', type=Path, default=Path.cwd(), help="absolute path of a mkCTF repository directory")

    def parse_args(self):
        '''Print the banner, parse arguments and configure some helpers using generic arguments
        '''
        if self._banner:
            app_log.info(self._banner)
        args = super().parse_args()
        log_enable_debug(args.debug)
        log_enable_logging(not args.quiet)
        app_log.debug(args)
        return args
