# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import json
from datetime import datetime
from slugify import slugify
from mkctf.helper.log import app_log
from mkctf.helper.cli import (
    Answer,
    choose,
    confirm,
    readline,
    readline_file,
    readline_files
)
# ==============================================================================
# CLASSES
# ==============================================================================
class ChallengeConfigurationWizard:
    '''[summary]
    '''
    def __init__(self, repo_conf, default):
        '''[summary]
        '''
        self._repo_conf = repo_conf
        # params
        self._name = default.get('name', "My New Challenge")
        self._slug = default.get('slug') # consistency: keep previous slug even if challenge renamed
        self._tags = default.get('tags')
        self._flag = default.get('flag') # consistency: keep previous flag even if challenge renamed
        self._author = default.get('author')
        self._points = default.get('points')
        self._enabled = default.get('enabled') # consistency: keep previous enabled even if challenge renamed
        self._category = default.get('category')
        self._logo_url = default.get('logo_url')
        self._difficulty = default.get('difficulty')
        self._static_url = default.get('static_url')

    @property
    def result(self):
        return {
            'name': self._name,
            'slug': self._slug,
            'tags': self._tags,
            'flag': self._flag,
            'author': self._author,
            'points': self._points,
            'enabled': self._enabled,
            'category': self._category,
            'logo_url': self._logo_url,
            'difficulty': self._difficulty,
            'static_url': self._static_url,
        }

    def show(self):
        while True:
            # - tags & difficulties
            self._name = readline(self._name, "Enter challenge display name")
            # consistency: keep previous slug even if challenge renamed
            self._slug = self._slug or slugify(self._name)
            self._tags = choose(self._repo_conf.tags, "Choose some tags or/and add custom ones",
                                min_count=1, multi=True)
            # consistency: keep previous flag even if challenge renamed
            self._flag = self._flag or self._repo_conf.make_rand_flag()
            self._author = readline(self._author, "Enter challenge author name")
            self._points = readline(self._points, "Enter challenge points or '-3' for dynamic")
            #self._enabled = self._enabled
            self._category = choose(self._repo_conf.categories, "Choose a category", min_count=1)
            self._logo_url = readline(self._logo_url, "Enter challenge logo url")
            self._tags = choose(self._repo_conf.difficulties, "Choose a difficulty", min_count=1)
            # consistency: keep previous enabled even if challenge renamed
            self._static_url = self._static_url or self._repo_conf.make_static_url(self._slug)
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=2)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
