# =============================================================================
#  IMPORTS
# =============================================================================
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
from mkctf.helper.formatting import format_text
# =============================================================================
#  CLASSES
# =============================================================================
class ColoredFormatter(Formatter):
    '''[summary]
    '''
    COLORS = {
        'DEBUG': 'green',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta'
    }

    def __init__(self, fmt=None, datefmt=None, style='%'):
        '''[summary]
        '''
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        '''[summary]
        '''
        os = super().format(record)
        return format_text(os, ColoredFormatter.COLORS[record.levelname])
# =============================================================================
#  GLOBALS
# =============================================================================
_fmtr = ColoredFormatter('[mkctf](%(levelname)s)> %(message)s')
_hdlr = StreamHandler()
_hdlr.setFormatter(_fmtr)
app_log = getLogger('mkctf')
app_log.setLevel(INFO)
app_log.addHandler(_hdlr)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def log_enable_debug(enable=True):
    '''[summary]
    '''
    app_log.setLevel(DEBUG if enable else INFO)

def log_enable_logging(enable=True):
    '''[summary]
    '''
    handlers = app_log.handlers
    if enable and _hdlr not in handlers:
        app_log.addHandler(_hdlr)
    elif not enable and _hdlr in handlers:
        app_log.removeHandler(_hdlr)
