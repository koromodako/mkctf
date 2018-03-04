# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: formatting.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
# =============================================================================
#  GLOBALS
# =============================================================================
TAB = ' ' * 4
EXIT_CODE_MAP = {
    None: ['TIMED-OUT', 'magenta'],
    0: ['SUCCESS', 'green'],
    2: ['N/A', 'grey'],
    3: ['MANUAL', 'yellow'],
    4: ['NOT-IMPLEMENTED', 'yellow']
}
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Sets the tab size.
##
## @param      size  The size
##
def set_tab_size(size):
    global TAB
    if size > 0:
        TAB = ' ' * size
##
## @brief      { function_description }
##
## @param      dictionary  The dictionary
##
def dict2str(dictionary):
    text = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            text += "\n+ {}:".format(key)
            text += dict2str(value).replace("\n", "\n{}".format(TAB))
        else:
            text += "\n+ {}: {}".format(key, value)
    return text
##
## @brief      { function_description }
##
## @param      status  The status
## @param      code    The code
##
def returncode2str(code, no_color):
    attrs = ['bold']
    value = EXIT_CODE_MAP.get(code)

    if value is None:
        value = ['FAILURE', 'red']

    status = '[{}]'.format(value[0])

    if code is not None:
        status += '(code={})'.format(code)

    if not no_color:
        status = colored(status, value[1], attrs=attrs)

    return status
