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
from termcolor import colored
from core.config import prog_prompt
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for logger.
##
class Logger(object):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      debug    The debug
    ## @param      verbose  The verbose
    ##
    def __init__(self, debug, quiet, no_color):
        super().__init__()
        self._debug = debug
        self._quiet = quiet
        self._no_color = no_color
    ##
    ## @brief      Prints message out using prog_prompt with given indicator
    ##
    ## @param      indicator  The indicator
    ## @param      msg        The message
    ## @param      end        The end
    ##
    def _print(self, indicator, color, msg, end, bold=False):
        if not self._quiet:
            line = "{}{}".format(prog_prompt(indicator), msg)
            if not self._no_color:
                attrs = ['bold'] if bold else []
                line = colored(line, color, attrs=attrs)
            print(line, end=end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def fatal(self, msg, end='\n'):
        self._print('FATAL', 'magenta', msg, end, bold=True)
        exit(1)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def error(self, msg, end='\n'):
        self._print('ERROR', 'red', msg, end, bold=True)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def warning(self, msg, end='\n'):
        self._print('WARNING', 'yellow', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def debug(self, msg, end='\n'):
        if self._debug:
            self._print('DEBUG', 'green', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def info(self, msg, end='\n'):
        self._print('INFO', 'blue', msg, end)
