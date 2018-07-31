'''
file: log.py
date: 2018-07-31
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from logging import getLogger, Formatter, LoggerAdapter, StreamHandler, DEBUG, INFO
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

class Python3FormatAdapater(LoggerAdapter):
    '''[summary]
    '''
    def log(self, lvl, msg, *args, **kwargs):
        '''[summary]
        '''
        if self.isEnabledFor(lvl):
            msg, kwargs = self.process(msg, kwargs)
            super().log(lvl, msg.format(*args, **kwargs))
# =============================================================================
#  GLOBALS
# =============================================================================
_fmtr = ColoredFormatter('[mkctf](%(levelname)s)> %(message)s')
_hdlr = StreamHandler()
_hdlr.setFormatter(_fmtr)
_logger = getLogger('mkctf')
_logger.setLevel(INFO)
_logger.addHandler(_hdlr)
app_log = Python3FormatAdapater(_logger, None)
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
    _logger.setLevel(DEBUG if debug else INFO)

def disable_logging():
    '''[summary]
    '''
    _logger.removeHandler(hdlr)
