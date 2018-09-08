'''
file: formatting.py
date: 2018-03-02
author: paul.dautry
purpose:

'''
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
def set_tab_size(size):
    '''Sets the tab size.

    Tabs are converted to spaces, this functions sets the size of a tabulation
    in spaces.

    Arguments:
        size {int} -- [description]
    '''
    global TAB
    if size > 0:
        TAB = ' ' * size

def dict2str(dictionary):
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
            text += dict2str(value).replace("\n", f"\n{TAB}")
        else:
            text += f"\n+ {key}: {value}"
    return text

def returncode2str(code, no_color):
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

    if not no_color:
        status = colored(status, value[1], attrs=attrs)

    return status
