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
    def __init__(self, debug, verbose):
        super().__init__()
        self.debug = debug
        self.verbose = verbose
    ##
    ## @brief      Prints message out using prog_prompt with given indicator
    ##
    ## @param      indicator  The indicator
    ## @param      msg        The message
    ## @param      end        The end
    ##
    def _print(self, indicator, msg, end):
        line = prog_prompt(indicator)
        line += msg
        print(line, end=end)
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
        if self.debug:
            self._print('DEBUG', msg, end)
    ##
    ## @brief      { function_description }
    ##
    ## @param      msg   The message
    ## @param      end   The end
    ##
    def info(self, msg, end='\n'):
        if self.verbose:
            self._print('INFO', msg, end)
