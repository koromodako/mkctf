# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import json
from datetime import datetime
from slugify import slugify
from mkctf.cli import (
    Answer,
    choose,
    confirm,
    readline,
)
from mkctf.helper.log import app_log
from mkctf.model.config import ChallengeConfiguration
# ==============================================================================
# CLASSES
# ==============================================================================
class ChallengeConfigurationWizard:
    '''[summary]
    '''
    def __init__(self, repo_conf, prev_conf=None):
        '''[summary]
        '''
        self._repo_conf = repo_conf
        # params
        if not prev_conf:
            prev_conf = {}
        self._name = prev_conf.get('name', "My New Challenge")
        self._slug = prev_conf.get('slug') # consistency: keep previous slug even if challenge renamed
        self._tags = prev_conf.get('tags')
        self._flag = prev_conf.get('flag') # consistency: keep previous flag even if challenge renamed
        self._author = prev_conf.get('author')
        self._points = prev_conf.get('points')
        self._enabled = prev_conf.get('enabled') # consistency: keep previous enabled even if challenge renamed
        self._category = prev_conf.get('category')
        self._logo_url = prev_conf.get('logo_url')
        self._difficulty = prev_conf.get('difficulty')
        self._static_url = prev_conf.get('static_url')

    @property
    def result(self):
        return ChallengeConfiguration({
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
        })

    def show(self):
        while True:
            # - tags & difficulties
            self._name = readline("Enter challenge display name", default=self._name)
            # consistency: keep previous slug even if challenge renamed
            self._slug = self._slug or slugify(self._name)
            self._tags = choose(self._repo_conf.tags, "Tags Selection",
                                min_count=1, multi=True)
            # consistency: keep previous flag even if challenge renamed
            self._flag = self._flag or self._repo_conf.make_rand_flag()
            self._author = readline("Enter challenge author name", default=self._author)
            self._points = readline("Enter challenge points or '-3' for dynamic", default=self._points)
            #self._enabled = self._enabled
            self._category = choose(self._repo_conf.categories, "Category Selection", min_count=1)
            self._logo_url = readline("Enter challenge logo url", default=self._logo_url)
            self._difficulty = choose(self._repo_conf.difficulties, "Difficulty Selection", min_count=1)
            # consistency: keep previous enabled even if challenge renamed
            self._static_url = self._static_url or self._repo_conf.make_static_url(self._slug)
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=2)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
