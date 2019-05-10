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
        self.default = {
            'name': prev_conf.get('name', "My New Challenge"),
            # consistency: keep previous slug even if challenge renamed
            'slug': prev_conf.get('slug'),
            'tags': prev_conf.get('tags'),
            # consistency: keep previous flag even if challenge renamed
            'flag': prev_conf.get('flag'),
            'author': prev_conf.get('author', ''),
            'points': prev_conf.get('points', -3),
            # consistency: keep previous enabled even if challenge renamed
            'enabled': prev_conf.get('enabled', False),
            'category': prev_conf.get('category'),
            'logo_url': prev_conf.get('logo_url', ''),
            'difficulty': prev_conf.get('difficulty'),
            'static_url': prev_conf.get('static_url'),
        }
        self._name = self.default['name']
        self._slug = self.default['slug']
        self._tags = self.default['tags']
        self._flag = self.default['flag']
        self._author = self.default['author']
        self._points = self.default['points']
        self._enabled = self.default['enabled']
        self._category = self.default['category']
        self._logo_url = self.default['logo_url']
        self._difficulty = self.default['difficulty']
        self._static_url = self.default['static_url']

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
            self._name = readline("Enter challenge display name", default=self.default['name'])
            # consistency: keep previous slug even if challenge renamed
            self._slug = self._slug or slugify(self._name)
            self._tags = choose(self._repo_conf.tags, "Tags Selection", multi=True)
            tags_str = '\n - '.join(self._tags)
            print(f"Selected tags:\n - {tags_str}")
            # consistency: keep previous flag even if challenge renamed
            self._flag = self._flag or self._repo_conf.make_rand_flag()
            self._author = readline("Enter challenge author name", empty=True, default=self.default['author'])
            self._points = readline("Enter challenge points or '-3' for dynamic", default=self.default['points'])
            #self._enabled = self._enabled
            self._category = choose(self._repo_conf.categories, "Category Selection")
            print(f"Selected category: {self._category}")
            self._logo_url = readline("Enter challenge logo url", empty=True, default=self._logo_url)
            self._difficulty = choose(self._repo_conf.difficulties, "Difficulty Selection")
            print(f"Selected difficulty: {self._difficulty}")
            # consistency: keep previous enabled even if challenge renamed
            self._static_url = self._static_url or self._repo_conf.make_static_url(self._slug)
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=2)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
