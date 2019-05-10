# =============================================================================
# IMPORTS
# =============================================================================
import re
import enum
from pick import pick
from mkctf.helper.log import app_log
# =============================================================================
# GLOBALS
# =============================================================================
INT_RE = re.compile(r'[\-]?[0-9]+')
# =============================================================================
# CLASSES
# =============================================================================
class Answer(enum.Enum):
    YES = 'y'
    NO = 'n'
    ABORT = 'abort'
# =============================================================================
# FUNCTIONS
# =============================================================================
def build_prompt(prompt, default=None):
    prompt = prompt.strip()
    if default is not None:
        prompt = f"{prompt} [{default}]"
    return f'{prompt}: '

def readline(prompt, empty=False, digit=False, default=None):
    '''Reads one line
    '''
    if isinstance(default, tuple):
        default_str = default[1]
        default = default[0]
    else:
        default_str = default
    value = ''
    while True:
        value = input(build_prompt(prompt, default_str))
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
    answers = []
    for answer in Answer:
        if not abort and answer == Answer.ABORT:
            continue
        if answer == default:
            answers.append(answer.value.upper())
        else:
            answers.append(answer.value)
    resp = readline(prompt, default=(Answer.NO.value, '/'.join(answers)))
    resp = resp.strip().lower()
    if resp in [Answer.YES.value, 'yes']:
        return Answer.YES
    elif abort and resp in [Answer.ABORT.value, 'a']:
        return Answer.ABORT
    return Answer.NO

def choose(choices, title, multi=False, min_count=1, custom=False):
    '''Elect one element among a collection

    You can also allow tht user to enter a custom value
    '''
    sep = '=' * ((78 - len(title)) // 2)
    title = f'{sep} {title} {sep}'
    text = [
        title,
        "",
        "Controls:",
        "    Arrow Up: move up",
        "  Arrow Down: move down",
        "    Spacebar: toggle selection",
        "       Enter: validate selection",
        ""
    ]
    if multi:
        plural = 's' if min_count > 1 else ''
        text.append(f"Choose {min_count} item{plural} or more from the list below then validate.")
    elif not multi and min_count == 1:
        text.append(f"Choose exactly one item from the list below then validate.")
    else:
        text.append(f"Choose an item from the list below (optional) then validate.")
    selection = pick(choices, '\n'.join(text), multi_select=multi, min_selection_count=min_count)
    if isinstance(selection, list):
        selection = [item[0] for item in selection]
    else:
        selection = selection[0]
    if custom:
        while True:
            selection_str = '\n - '.join(selection)
            prompt = f"Do you want to add a custom value to current selection: \n - {selection_str}\nEnter your answer"
            if confirm(prompt) == Answer.NO:
                break
            selection.append(readline("Enter a custom value", empty=False))
    return selection

