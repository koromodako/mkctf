# ==============================================================================
#  IMPORTS
# ==============================================================================
from argparse import ArgumentParser
from .log import app_log, log_enable_debug, log_enable_logging
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFArgumentParser(ArgumentParser):
    '''A specialised argument parser to define common arguments
    '''
    def __init__(self, banner, description):
        '''Construct a mkCTF argument parser
        '''
        super().__init__(add_help=True, description=description)
        self._banner = banner
        self.add_argument('--quiet', '-q', action='store_true', help="disable logging")
        self.add_argument('--debug', '-d', action='store_true', help="enable debug messages")
        self.add_argument('--repo-dir', '-r', type=Path, default=Path.cwd(), help="absolute path of a mkCTF repository directory")

    def parse_args(self):
        '''Print the banner, parse arguments and configure some helpers using generic arguments
        '''
        app_log.info(self._banner)
        args = super().parse_args()
        log_enable_debug(args.debug)
        log_enable_logging(not args.quiet)
        app_log.debug(args)
        return args
