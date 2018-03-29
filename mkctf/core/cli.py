# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: cli.py
#    date: 2017-07-23
#  author: paul.dautry
# purpose:
#    Utils CLI-related functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# =============================================================================
from shutil import which
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from mkctf.core.config import prog_prompt
# =============================================================================
# CLASSES
# =============================================================================


class CLI(object):
    """Command line interaction utility

    Provides useful methods to read user input.
    """
    def __init__(self, logger):
        """[summary]

        [description]

        Arguments:
            logger {[type]} -- [description]
        """
        super().__init__()
        self.logger = logger
        self.prog_prompt = prog_prompt('?').strip()

    def prompt(self, prompt):
        """[summary]

        [description]

        Arguments:
            prompt {[type]} -- [description]
        """
        return "{} {} ".format(self.prog_prompt, prompt.strip())

    def readline(self,
                 prompt,
                 allow_empty=False,
                 expect_digit=False,
                 default=None):
        """Reads one line

        Arguments:
            prompt {str} -- [description]

        Keyword Arguments:
            allow_empty {bool} -- [description] (default: {False})
            expect_digit {bool} -- [description] (default: {False})
            default {str or None} -- [description] (default: {None})

        Returns:
            str -- [description]
        """
        value = ''

        if not isinstance(prompt, str):
            raise ValueError("prompt argument must be a string.")

        if default is not None:

            if expect_digit:
                if not isinstance(default, int):
                    raise ValueError("default argument must be an integer.")

            elif not isinstance(default, str):
                raise ValueError("default argument must be an string.")

            prompt = "{} [default={}] ".format(prompt.strip(), default)

        full_prompt = self.prompt(prompt)

        while True:
            value = input(full_prompt)

            if len(value) > 0:

                if expect_digit and not value.isdigit():
                    self.logger.error("answer must be a digit.")
                    continue

                break

            if default is not None:
                return default

            if allow_empty:
                return None

            self.logger.error("empty answer is not allowed.")

        if expect_digit:
            value = int(value, 0)

        return value

    def readlines(self, prompt, subprompt, expect_digit=False):
        """Reads multiple lines

        Stops when the line contains a single dot ('.') character.

        Arguments:
            prompt {str} -- [description]
            subprompt {str} -- [description]

        Keyword Arguments:
            expect_digit {bool} -- [description] (default: {False})

        Returns:
            str -- [description]
        """
        lines = []

        print(self.prompt(prompt))
        while True:
            value = self.readline(subprompt, True, expect_digit)

            if value == '.':
                break

            lines.append(value)

        return lines

    def confirm(self, question, default=False):
        """Asks user for confirmation

        Arguments:
            question {str} -- [description]

        Keyword Arguments:
            default {bool} -- [description] (default: {False})
        """
        default = 'true' if default else 'false'
        resp = self.readline(question.strip(),
                             default=default)
        return (resp.strip().lower() in ['true', 'y', 'yes', '1'])

    def choose_one(self,
                   prompt,
                   choices,
                   default=None,
                   allow_custom=False):
        """Elect one element among a collection

        You can also allow tht user to enter a custom value

        Arguments:
            prompt {str} -- [description]
            choices {list(any)} -- [description]

        Keyword Arguments:
            default {any} -- [description] (default: {None})
            allow_custom {bool} -- [description] (default: {False})

        Returns:
            any -- [description]
        """
        selection = default

        if not isinstance(choices, list): # do not check number of elements
            raise ValueError("choices must be a list")

        has_default = default is not None

        if has_default and not default in choices:
            raise ValueError("default value must be one of choices.")

        print(self.prompt(prompt))

        k = 0
        for choice in choices:

            default_str = ''
            if choice == default:
                default_str = ' [default]'

            print("\t{:02d}: {}{}".format(k, choices[k], default_str))
            k += 1

        if allow_custom:
            print("\t{:02d}: custom value".format(k))

        while True:
            choice = self.readline("enter a number: ",
                                   allow_empty=has_default,
                                   expect_digit=True)

            if choice is None:
                return default

            if choice >= 0 or choice <= k:
                break

            self.logger.error("input must be in [0,{}]".format(k))

        if allow_custom and choice == k:
            selection = self.readline("enter custom value: ")
        else:
            selection = choices[choice]

        return selection

    def choose_many(self,
                    prompt,
                    choices,
                    default=None,
                    min_choices=None,
                    max_choices=None,
                    allow_custom=False,
                    allow_multiple=False):
        """Elect many elements among a collection

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
        """
        if min_choices is not None:
            if min_choices < 1:
                raise ValueError("min_choices argument must be strictly "
                                 "greater than 1 if not None.")
        else:
            min_choices = 1

        if max_choices is not None and max_choices < min_choices:
            raise ValueError("max_choices argument must be greater than {} if "
                             "not None.".format(min_choices))

        if default is not None:
            if not isinstance(default, list):
                raise ValueError("default argument must be a list.")

            length = len(default)
            if length < min_choices:
                raise ValueError("default list must respect min_choices value.")

            if max_choices is not None and length > max_choices:
                raise ValueError("default list must respect max_choices value.")

        print(self.prompt(prompt))

        if default is not None:
            print("default selection: {}".format(default))
            if self.confirm("do you want the default selection?"):
                return default

        count = 0
        selection = []
        remaining = choices[::]
        while True:
            print("current selection: {}".format(selection))
            choice = self.choose_one(prompt, remaining, None, allow_custom)
            selection.append(choice)
            count += 1

            if not allow_multiple and choice in remaining:
                remaining.remove(choice)

            if count >= min_choices:
                if max_choices is not None and count == max_choices:
                    if self.confirm("maximum selection size reached, do you "
                                    "want to reset?"):
                        count = 0
                        selection = []
                        remaining = choices[::]
                        continue
                    else:
                        break

                if not self.confirm("do you want to continue?"):
                    break

        return selection
