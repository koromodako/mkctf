# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: formatting.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  GLOBALS
# =============================================================================
TAB = ' ' * 4
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
