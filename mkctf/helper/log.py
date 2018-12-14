'''
file: log.py
date: 2018-07-31
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
from mkctf.helper.win import WINDOWS
if not WINDOWS:
    from termcolor import colored
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
        self._no_color = WINDOWS

    def disable_color(self):
        self._no_color = False

    def format(self, record):
        '''[summary]
        '''
        os = super().format(record)
        if not self._no_color:
            os = colored(os, ColoredFormatter.COLORS[record.levelname])
        return os
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
def disable_color():
    '''[summary]
    '''
    _fmtr.disable_color()

def enable_debug(debug=True):
    '''[summary]
    '''
    app_log.setLevel(DEBUG if debug else INFO)

def disable_logging():
    '''[summary]
    '''
    app_log.removeHandler(hdlr)
