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
from core.config import prog_prompt
# =============================================================================
# CLASSES
# =============================================================================
##
## @brief      Class for cli.
##
class CLI(object):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      logger  The logger
    ##
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.prog_prompt = prog_prompt('?').strip()
    ##
    ## @brief      { function_description }
    ##
    ## @param      prompt  The prompt
    ##
    def prompt(self, prompt):
        return "{} {} ".format(self.prog_prompt, prompt.strip())
    ##
    ## @brief      Reads one line.
    ##
    ## @param      prompt        The prompt
    ## @param      allow_empty   The allow empty
    ## @param      default       The default
    ## @param      expect_digit  The expect digit
    ##
    def readline(self,
                 prompt,
                 allow_empty=False,
                 expect_digit=False,
                 default=None):
        value = ''

        if not isinstance(prompt, str):
            raise ValueError("prompt argument must be a string.")

        if default is not None:

            if expect_digit and not isinstance(default, int):
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
    ##
    ## @brief      Reads multiple lines.
    ##
    ## @param      prompt        The prompt
    ## @param      subprompt     The subprompt
    ## @param      expect_digit  The expect digit
    ##
    ## @return     { description_of_the_return_value }
    ##
    def readlines(self, prompt, subprompt, expect_digit=False):
        lines = []

        print(self.prompt(prompt))
        while True:
            value = self.readline(subprompt, True, expect_digit)

            if value == '.':
                break

            lines.append(value)

        return lines
    ##
    ## @brief      Asks user for confirmation
    ##
    ## @param      question  The question
    ##
    ## @return     { description_of_the_return_value }
    ##
    def confirm(self, question, default=False):
        default = 'true' if default else 'false'
        resp = self.readline(question.strip(),
                             default=default)
        return (resp.strip().lower() in ['true', 'y', 'yes', '1'])
    ##
    ## @brief      Choose one among choices and possibly a custom value
    ##
    ## @param      prompt        The prompt
    ## @param      choices       The choices
    ## @param      allow_custom  The allow custom
    ##
    def choose_one(self,
                   prompt,
                   choices,
                   default=None,
                   allow_custom=False):
        selection = default

        if not isinstance(choices, list) or len(choices) < 2:
            raise ValueError("choices must be a list with at least 2 elements.")

        if default is not None and not default in choices:
            raise ValueError("default value must be one of choices.")

        print(self.prompt(prompt))

        k = 0
        for choice in choices:

            is_default = ''
            if choice == default:
                is_default = ' [default]'

            print("\t{:02d}: {}{}".format(k, choices[k], is_default))
            k += 1

        if default is not None:
            print("\t{:02d}: default value".format(k))
            k += 1

        if allow_custom:
            print("\t{:02d}: custom value".format(k))

        while True:
            choice = self.readline("enter a number: ", expect_digit=True)

            if choice >= 0 or choice <= k:
                break

            self.logger.error("input must be in [0,{}]".format(k))

        if allow_custom and choice == k:
            selection = self.readline("enter custom value: ")
        elif default is not None and choice == (k-1):
            pass
        else:
            selection = choices[choice]

        return selection
    ##
    ## @brief      { function_description }
    ##
    ## @param      prompt             The prompt
    ## @param      choices            The choices
    ## @param      allow_custom       The allow custom
    ## @param      default_selection  The default selection
    ## @param      min                The minimum
    ## @param      max                The maximum
    ##
    def choose_many(self,
                    prompt,
                    choices,
                    default=None,
                    min_choices=None,
                    max_choices=None,
                    allow_custom=False,
                    allow_multiple=False):
        if min_choices is not None:
            if min_choices < 2:
                raise ValueError("min_choices argument must be strictly "
                                 "greater than 1 if not None.")
        else:
            min_choices = 2

        if max_choices is not None and max_choices < min_choices:
            raise ValueError("max_choices argument must be greater than {} if "
                             "not None.".format(min_choices))

        if default is not None:
            if not isinstance(default, list):
                raise ValueError("default argument must be a list.")

            length = len(default)
            if length < min_choices and length > max_choices:
                raise ValueError("default list must match min/max "
                                 "requirements.")

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
