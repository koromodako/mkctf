#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    utils.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       Implements some helpers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from core.logger import Logger

def read_input(prompt, allow_empty=False, expect_digit=False):
    """read_input"""
    uinput = ''
    if not isinstance(prompt, str):
        Logger.err('read_input prompt argument must be a string.')
    full_prompt = '[?] > ' + prompt
    uinput = input(full_prompt)
    while not allow_empty and len(uinput) == 0:
        Logger.err('empty answer is not allowed.')
        uinput = input(full_prompt)
    while expect_digit and not uinput.isdigit():
        Logger.err('answer must be a digit.')
        uinput = input(full_prompt)
    if expect_digit:
        uinput = int(uinput, 10)
    return uinput

def select_category(categories):
    """select_categories"""
    uinput = -1
    if not isinstance(categories, list):
        Logger.err('select_category categories argument must be a list.')
    k = 0
    for category in categories:
        print('\t%d - %s' % (k, category))
        k += 1
    while uinput < 0 or uinput > len(categories):
        uinput = read_input('please select a category using its number: ', False, True)
    return categories[uinput]
