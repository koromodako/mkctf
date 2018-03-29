# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: logger.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import sys
from termcolor import colored
from core.config import prog_prompt
# =============================================================================
#  CLASSES
# =============================================================================

class Logger(object):
    """Application logger

    Provides methods to log messages lighter than using python's
    logging module
    """
    def __init__(self, debug, quiet, no_color, out=None):
        """Constructor

        Arguments:
            debug {bool} -- [description]
            quiet {bool} -- [description]
            no_color {bool} -- [description]

        Keyword Arguments:
            out {io.IOBase} -- [description] (default: {None})
        """
        super().__init__()
        self._debug = debug
        self._quiet = quiet
        self._no_color = no_color
        self._out = out or sys.stderr

    def _print(self, indicator, color, msg, end, bold=False):
        """Prints message out using prog_prompt with given indicator

        [description]

        Arguments:
            indicator {str} -- [description]
            color {str} -- [description]
            msg {str} -- [description]
            end {str} -- [description]

        Keyword Arguments:
            bold {bool} -- [description] (default: {False})
        """
        if not self._quiet:
            line = "{}{}".format(prog_prompt(indicator), msg)
            if not self._no_color:
                attrs = ['bold'] if bold else []
                line = colored(line, color, attrs=attrs)
            self._out.write('{}{}'.format(line, end))

    def fatal(self, msg, end='\n'):
        """Logs a fatal message and exists the application

        Return code value is 101, just for fun

        Arguments:
            msg {str} -- [description]

        Keyword Arguments:
            end {str} -- [description] (default: {'n'})
        """
        self._print('FATAL', 'magenta', msg, end, bold=True)
        exit(101)

    def error(self, msg, end='\n'):
        """Logs an error message

        Arguments:
            msg {str} -- [description]

        Keyword Arguments:
            end {str} -- [description] (default: {'n'})
        """
        self._print('ERROR', 'red', msg, end, bold=True)

    def warning(self, msg, end='\n'):
        """Logs a warning message

        Arguments:
            msg {str} -- [description]

        Keyword Arguments:
            end {str} -- [description] (default: {'n'})
        """
        self._print('WARNING', 'yellow', msg, end)

    def debug(self, msg, end='\n'):
        """Logs a debugging-related message

        Arguments:
            msg {str} -- [description]

        Keyword Arguments:
            end {str} -- [description] (default: {'n'})
        """
        if self._debug:
            self._print('DEBUG', 'green', msg, end)

    def info(self, msg, end='\n'):
        """Logs an informative message

        Arguments:
            msg {[type]} -- [description]

        Keyword Arguments:
            end {str} -- [description] (default: {'n'})
        """
        self._print('INFO', 'blue', msg, end)
