# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.helper.win import WINDOWS
if not WINDOWS:
    from termcolor import colored
# =============================================================================
#  GLOBALS
# =============================================================================
TAB = ' ' * 4
HSEP = '-' * 80
COLORIZE = not WINDOWS
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
def format_enable_colors(enable):
    global COLORIZE
    COLORIZE = enable

def format_text(text, color, attrs=None):
    if not attrs:
        attrs = []
    if COLORIZE:
        return colored(text, color, attrs=attrs)
    return text

def format_set_tab_size(size):
    '''Sets the tab size.

    Tabs are converted to spaces, this functions sets the size of a tabulation
    in spaces.

    Arguments:
        size {int} -- [description]
    '''
    global TAB
    if size > 0:
        TAB = ' ' * size

def format_dict2str(dictionary):
    '''Converts a dictionary recursively into human-readable nested lists

    >>> d = {'a': 1, 'b': 2, 'c': { 4: ['a', 'b'] }}
    >>> print(dict2str(d))
    + a: 1
    + b: 2
    + c:
        + 4: ['a', 'b']

    Arguments:
        dictionary {dict} -- [description]
    '''
    text = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            text += f"\n+ {key}:"
            text += format_dict2str(value).replace("\n", f"\n{TAB}")
        else:
            text += f"\n+ {key}: {value}"
    return text

def format_rcode2str(code):
    '''[summary]

    [description]

    Arguments:
        code {int or None} -- [description]
        no_color {bool} -- [description]
    '''
    attrs = ['bold']
    value = EXIT_CODE_MAP.get(code)
    if value is None:
        value = ['FAILURE', 'red']
    status = f'[{value[0]}]'
    if code is not None:
        status += f'(code={code})'
    return format_text(status, value[1], attrs)
