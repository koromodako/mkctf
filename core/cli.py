# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: cli.py
#    date: 2017-07-23
#  author: paul.dautry
# purpose:
#    Utils CLI-related functions
# license:
#    Utils
#    Copyright (C) 2017  Paul Dautry
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
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
    ##
    ## @brief      Reads an input.
    ##
    ## @param      prompt        The prompt
    ## @param      allow_empty   The allow empty
    ## @param      expect_digit  The expect digit
    ##
    ## @return     { description_of_the_return_value }
    ##
    def read_input(self, prompt, allow_empty=False, expect_digit=False):
        uinput = ''

        if not isinstance(prompt, str):
            self.logger.error("read_input prompt argument must be a string. (dev)")

        full_prompt = prog_prompt('?') + prompt

        uinput = input(full_prompt)

        while not allow_empty and len(uinput) == 0:
            self.logger.error("empty answer is not allowed.")
            uinput = input(full_prompt)

        while expect_digit and not uinput.isdigit():
            self.logger.error("answer must be a digit.")
            uinput = input(full_prompt)

        if expect_digit:
            uinput = int(uinput, 10)

        return uinput
    ##
    ## @brief      Reads an multiple inputs.
    ##
    ## @param      prompt        The prompt
    ## @param      subprompt     The subprompt
    ## @param      expect_digit  The expect digit
    ##
    ## @return     { description_of_the_return_value }
    ##
    def read_input_loop(self, prompt, subprompt, expect_digit=False):
        out = []
        print(prog_prompt("?") + prompt)

        uinput = self.read_input(subprompt, True, expect_digit)
        while uinput != "." and len(uinput) > 0:
            out.append(uinput)
            uinput = self.read_input(subprompt, False, expect_digit)

        return out
    ##
    ## @brief      Asks user for confirmation
    ##
    ## @param      question  The question
    ##
    ## @return     { description_of_the_return_value }
    ##
    def confirm(self, question):
        resp = self.read_input("%s [y/*]: " % question)
        return (resp.lower() == 'y')
    ##
    ## @brief      Choice one value from a list of 2..N values
    ##
    ## @param      prompt  The prompt
    ## @param      among   The among
    ##
    ## @return     { description_of_the_return_value }
    ##
    def choose_one(self, prompt, among):
        if not isinstance(among, list) or len(among) < 2:
            raise ValueError("among must be a list with at least 2 elements.")

        print(prog_prompt("?") + prompt)
        for i in range(len(among)):
            print("\t%02d: %s" % (i, among[i]))

        uinput = self.read_input("select a number: ", expect_digit=True)
        while uinput < 0 or uinput >= len(among):
            self.logger.error("input must be in [0,%d]" % (len(among)-1))
            uinput = self.read_input('select a number: ', expect_digit=True)

        return among[uinput]
    ##
    ## @brief      Check if commands are available on the system
    ##
    ## @param      commands  Commands to look for
    ##
    ## @return     { description_of_the_return_value }
    ##
    def look_for_commands(self, commands):
        if not isinstance(commands, list):
            raise ValueError("self.look_for_commands expects 'commands' to be "
                             "a list.")

        for cmd in commands:
            if which(cmd) is None:
                self.logger.error("'{}' command seems to be unavailable.".format(cmd))
                return False

        return True
    ##
    ## @brief      Executes command passed as a list of arguments
    ##
    ## @param      args  Arguments
    ##
    def exec(self, args):
        self.logger.info("exec cmd: {}".format(' '.join(args)))
        call(args)
    ##
    ## @brief      Executes command passed as a string
    ##
    ## @param      cmd   The command
    ##
    def exec_shell(self, cmd):
        self.logger.info("exec cmd: {}".format(cmd))
        call(cmd, shell=True)
    ##
    ## @brief      Starts a proc.
    ##
    ## @param      args             Arguments used to start the process
    ## @param      wait             True if function should wait for spawned
    ##                              process to terminate before returning it
    ## @param      capture_outputs  True if command should capture stdout and
    ##                              stderr
    ## @param      cwd              Current Working Directory
    ##
    ## @return     subprocess.Process
    ##
    def start_proc(self, args, wait=True, capture_outputs=False, cwd=None):
        self.logger.info("start process with: {}".format(' '.join(args)))
        kwargs = {}

        if cwd is not None:
            kwargs['cwd'] = cwd

        if capture_outputs:
            kwargs['stdout'] = PIPE
            kwargs['stderr'] = PIPE

        p = Popen(args, **kwargs)

        if wait:
            p.wait()

        return p
