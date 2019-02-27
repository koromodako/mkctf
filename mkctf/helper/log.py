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
def enable_debug(debug=True):
    '''[summary]
    '''
    app_log.setLevel(DEBUG if debug else INFO)

def disable_logging():
    '''[summary]
    '''
    app_log.removeHandler(_hdlr)
