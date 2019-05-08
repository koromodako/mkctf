# =============================================================================
# IMPORTS
# =============================================================================
import re
import enum
from pick import pick
from .log import app_log
# =============================================================================
# GLOBALS
# =============================================================================
INT_RE = re.compile(r'[\-]?[0-9]+')
# =============================================================================
# CLASSES
# =============================================================================
class Answer(enum.Enum):
    NO = 'no'
    YES = 'yes'
    ABORT = 'abort'
# =============================================================================
# FUNCTIONS
# =============================================================================
def build_prompt(prompt, default=None):
    prompt = prompt.strip()
    if default is not None:
        prompt = f"{prompt} [{default}]"
    return f'{prompt}:'

def readline(default, prompt, empty=False, digit=False):
    '''Reads one line
    '''
    value = ''
    while True:
        value = input(build_prompt(prompt))
        if len(value) > 0:
            if digit and not INT_RE.fullmatch(value):
                app_log.error("answer must be a digit.")
                continue
            break
        if default is not None:
            return default
        if empty:
            return None
        app_log.error("empty answer is not allowed.")
    if digit:
        value = int(value, 0)
    return value

def confirm(prompt, default=Answer.NO, abort=False):
    '''Asks user for confirmation
    '''
    default_str = []
    for answer in Answer:
        if not abort and answer.ABORT:
            continue
        if answer == default:
            default_str.append(answer.name.upper())
        else:
            default_str.append(answer.name)
    default_str = '/'.join(default_str)
    prompt = build_prompt(prompt.strip(), default_str)
    resp = readline(prompt, default=default.name)
    resp = resp.strip().lower()
    if not resp:
        return default
    if resp in [Answer.YES.name, 'y']:
        return Answer.YES
    elif abort and resp in [Answer.ABORT.name, 'a']:
        return Answer.ABORT
    return Answer.NO

def choose(choices, prompt, min_count=0, multi=False, custom=False):
    '''Elect one element among a collection

    You can also allow tht user to enter a custom value
    '''
    selection = pick(choices, prompt, multi_select=multi, min_selection_count=min_count)
    if custom:
        while True:
            prompt = f"Do you want to add a custom value to current selection: \n - {'\n - '.join(selection)}"
            if confirm(prompt) == Answer.NO:
                break
            selection.append(readline('custom-value', "Enter a custom value", empty=False))
    return selection

