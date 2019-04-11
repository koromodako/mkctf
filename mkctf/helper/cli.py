# =============================================================================
# IMPORTS
# =============================================================================
import re
from mkctf.helper.log import app_log
# =============================================================================
# GLOBALS
# =============================================================================
INT_RE = re.compile(r'[\-]?[0-9]+')
PROG_PROMPT = f"[mkctf](?)>"
# =============================================================================
# CLASSES
# =============================================================================
def get_prompt(prompt):
    '''Creates a specific prompt
    '''
    prompt = prompt.strip()
    return f"{PROG_PROMPT} {prompt} "

def readline(prompt, allow_empty=False, expect_digit=False, default=None):
    '''Reads one line
    '''
    value = ''
    if not isinstance(prompt, str):
        raise ValueError("prompt argument must be a string.")

    if default is not None:
        if expect_digit:
            if not isinstance(default, int):
                raise ValueError("default argument must be an integer.")
        elif not isinstance(default, str):
            raise ValueError("default argument must be an string.")
        prompt = prompt.strip()
        prompt = f"{prompt} [default={default}] "
    full_prompt = get_prompt(prompt)
    while True:
        value = input(full_prompt)
        if len(value) > 0:
            if expect_digit and not INT_RE.fullmatch(value):
                app_log.error("answer must be a digit.")
                continue
            break
        if default is not None:
            return default
        if allow_empty:
            return None
        app_log.error("empty answer is not allowed.")
    if expect_digit:
        value = int(value, 0)
    return value

def readlines(prompt, subprompt, expect_digit=False):
    '''Reads multiple lines

    Stops when the line contains a single dot ('.') character.
    '''
    lines = []
    print(get_prompt(prompt))
    while True:
        value = readline(subprompt, True, expect_digit)
        if value == '.':
            break
        lines.append(value)
    return lines

def confirm(question, default=False):
    '''Asks user for confirmation
    '''
    default = 'true' if default else 'false'
    resp = readline(question.strip(), default=default)
    return (resp.strip().lower() in ['true', 'y', 'yes', '1'])

def choose_one(prompt, choices, default=None, allow_custom=False):
    '''Elect one element among a collection

    You can also allow tht user to enter a custom value
    '''
    selection = default
    if not isinstance(choices, list): # do not check number of elements
        raise ValueError("choices must be a list")
    has_default = default is not None
    if has_default and not default in choices:
        raise ValueError("default value must be one of choices.")
    print(get_prompt(prompt))
    k = 0
    for choice in choices:
        default_str = ''
        if choice == default:
            default_str = ' [default]'
        print(f"\t{k:02d}: {choices[k]}{default_str}")
        k += 1
    if allow_custom:
        print(f"\t{k:02d}: custom value")
    while True:
        choice = readline("enter a number: ", allow_empty=has_default, expect_digit=True)
        if choice is None:
            return default
        if choice >= 0 or choice <= k:
            break
        app_log.error(f"input must be in [0,{k}]")
    if allow_custom and choice == k:
        selection = readline("enter custom value: ")
    else:
        selection = choices[choice]
    return selection

def choose_many(prompt,
                choices,
                default=None,
                min_choices=None,
                max_choices=None,
                allow_custom=False,
                allow_multiple=False):
    '''Elect many elements among a collection

    Arguments:
        prompt {str} -- [description]
        choices {list(any)} -- [description]

    Keyword Arguments:
        default {any} -- [description] (default: {None})
        min_choices {int(1,)} -- [description] (default: {None})
        max_choices {int(min_choices,)} -- [description] (default: {None})
        allow_custom {bool} -- [description] (default: {False})
        allow_multiple {bool} -- [description] (default: {False})

    Returns:
        list(any) -- [description]
    '''
    if min_choices is not None:
        if min_choices < 1:
            raise ValueError("min_choices argument must be strictly "
                             "greater than 1 if not None.")
    else:
        min_choices = 1
    if max_choices is not None and max_choices < min_choices:
        raise ValueError(f"max_choices argument must be greater than {min_choices} if not None.")
    if default is not None:
        if not isinstance(default, list):
            raise ValueError("default argument must be a list.")
        length = len(default)
        if length < min_choices:
            raise ValueError("default list must respect min_choices value.")
        if max_choices is not None and length > max_choices:
            raise ValueError("default list must respect max_choices value.")
    print(get_prompt(prompt))
    if default is not None:
        print(f"default selection: {default}")
        if confirm("do you want the default selection?"):
            return default
    count = 0
    selection = []
    remaining = choices[::]
    while True:
        print(f"current selection: {selection}")
        choice = choose_one(prompt, remaining, None, allow_custom)
        selection.append(choice)
        count += 1
        if not allow_multiple and choice in remaining:
            remaining.remove(choice)
        if count >= min_choices:
            if max_choices is not None and count == max_choices:
                if confirm("maximum selection size reached, do you want to reset?"):
                    count = 0
                    selection = []
                    remaining = choices[::]
                    continue
                else:
                    break
            if not confirm("do you want to continue?"):
                break
    return selection
