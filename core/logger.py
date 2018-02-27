# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: logger.py
#     date: 2018-02-27
#   author: paul.dautry
#  purpose:
#
#  license:
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
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
    def __init__(self, debug, quiet):
        super().__init__()
        self._debug = debug
        self._quiet = quiet
    ##
    ## @brief      Prints message out using prog_prompt with given indicator
    ##
    ## @param      indicator  The indicator
    ## @param      msg        The message
    ## @param      end        The end
    ##
    def _print(self, indicator, msg, end):
        if not self._quiet:
            print("{}{}".format(prog_prompt(indicator), msg), end=end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def fatal(self, msg, end='\n'):
        self._print('FATAL', msg, end)
        exit(1)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def error(self, msg, end='\n'):
        self._print('ERROR', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def warning(self, msg, end='\n'):
        self._print('WARNING', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def debug(self, msg, end='\n'):
        if self._debug:
            self._print('DEBUG', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def info(self, msg, end='\n'):
        self._print('INFO', msg, end)
