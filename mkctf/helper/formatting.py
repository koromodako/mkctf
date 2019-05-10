# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
# =============================================================================
#  GLOBALS
# =============================================================================
TAB = ' ' * 2
HSEP = '-' * 80
EXIT_CODE_MAP = {
    None: ('TIMEOUT', 'magenta'),
    0: ('SUCCESS', 'green'),
    2: ('N/A', 'grey'),
    3: ('MANUAL', 'yellow'),
    4: ('NOT-IMPLEMENTED', 'yellow'),
}
HEALTHY_EXIT_CODES = {0, 2, 3}
# =============================================================================
#  FUNCTIONS
# =============================================================================
def format_text(text, color, attrs=None):
    '''Wrap text in ANSI tags
    '''
    if not attrs:
        attrs = []
    return colored(text, color, attrs=attrs)

def format_set_tab_size(size):
    '''Set the tab size.

    Tabs are converted to spaces, this functions sets the size of a tabulation
    in spaces.

    Arguments:
        size {int} -- [description]
    '''
    global TAB
    if size > 0:
        TAB = ' ' * size

def format_dict2str(dictionary):
    '''Convert a dictionary recursively into human-readable nested lists

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
    '''
    attrs = ['bold']
    status, color = EXIT_CODE_MAP.get(code, ('FAILURE', 'red'))
    status = f'[{status}]'
    if code is not None:
        status += f'(code={code})'
    return format_text(status, color, attrs)

def format_rcode2health(code):
    '''[summary]
    '''
    attrs = ['bold']
    color = 'red'
    status = 'UNHEALTHY'
    if code in HEALTHY_EXIT_CODES:
        color = 'green'
        status = 'HEALTHY'
    return format_text(f'[{status}]', color, attrs)
