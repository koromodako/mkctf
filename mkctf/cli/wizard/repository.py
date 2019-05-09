# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import json
from datetime import datetime
from mkctf.cli import (
    Answer,
    choose,
    confirm,
    readline,
)
from mkctf.helper.log import app_log
from mkctf.model.config import RepositoryConfiguration
# ==============================================================================
# CLASSES
# ==============================================================================
class RepositoryConfigurationWizard:
    '''[summary]
    '''
    def __init__(self, general_conf, prev_conf=None):
        if not prev_conf:
            prev_conf = {}
        self._name = f'Example CTF {datetime.now().year}'
        # - tags & difficulties
        self._tags = prev_conf.get('tags', general_conf.tags)
        self._difficulties = prev_conf.get('difficulties', general_conf.difficulties)
        # - flag
        self._flag_prefix = prev_conf.get('flag', {}).get('prefix', general_conf.flag_prefix)
        self._flag_suffix = prev_conf.get('flag', {}).get('suffix', general_conf.flag_suffix)
        # - domain
        self._domain = prev_conf.get('domain', general_conf.domain)
        # - docker
        self._docker_user = prev_conf.get('docker', {}).get('user', general_conf.docker_user)
        self._docker_registry = prev_conf.get('docker', {}).get('registry', general_conf.docker_registry)

    @property
    def result(self):
        return RepositoryConfiguration({
            'name': self._name,
            'tags': self._tags,
            'difficulties': self._difficulties,
            'flag': {
                'prefix': self._flag_prefix,
                'suffix': self._flag_suffix,
            },
            'domain': self._domain,
            'docker': {
                'user': self._docker_user,
                'registry': self._docker_registry,
            },
            'static': {
                'salt': os.urandom(16).hex(),
                'base_url': f'https://static.{self._domain}/'
            },
            'standard': {
                'dirs': {
                    'public': ['public-files'],
                    'private': ['healthcheck'],
                },
                'build': {
                    'name': 'build',
                    'from': 'build.jinja'
                },
                'deploy': {
                    'name': 'deploy',
                    'from': 'deploy.jinja'
                },
                'healthcheck': {
                    'name': 'healthcheck/healthcheck',
                    'from': 'healthcheck.jinja'
                },
                'description': {
                    'name': 'public-files/description.md',
                    'from': 'description.md.jinja'
                },
                'files': [
                    {
                        'name': '.gitignore'
                    },
                    {
                        'name': 'writeup.md',
                        'from': ''
                    },
                    {
                        'name': 'healthcheck/healthcheck.deps',
                        'from': 'healthcheck.deps'
                    },
                ],
            },
            'categories': {
                'simple': {
                    'dirs': {
                        'public': [],
                        'private': [
                            'private-files'
                        ],
                    },
                    'files': [],
                },
                'server': {
                    'dirs': {
                        'public': [],
                        'private': [
                            'server-files'
                        ],
                    },
                    'files': [
                        {
                            'name': 'server-files/Dockerfile',
                            'from': 'Dockerfile.server'
                        },
                    ],
                },
                'sandbox': {
                    'dirs': {
                        'public': [],
                        'private': [
                            'server-files'
                        ],
                    },
                    'files': [
                        {
                            'name': 'server-files/Dockerfile',
                            'from': 'Dockerfile.sandbox-server'
                        },
                        {
                            'name': 'server-files/Dockerfile.sandbox',
                            'from': 'Dockerfile.server'
                        },
                        {
                            'name': 'server-files/banner',
                            'from': 'banner'
                        },
                        {
                            'name': 'server-files/sshd_config',
                            'from': 'sshd_config'
                        },
                        {
                            'name': 'server-files/sandbox_start.sh',
                            'exec': True,
                            'from': 'sandbox_start.sh.jinja'
                        },
                    ],
                },
            },
        })

    def show(self):
        while True:
            self._name = readline("Enter a name", default=self._name)
            # - tags & difficulties
            self._tags = choose(self._tags, "Tags Selection", min_count=2, multi=True, custom=True)
            tags_str = '\n - '.join(self._tags)
            print(f"Selected tags:\n - {tags_str}")
            self._difficulties = choose(self._difficulties, "Difficulties Selection",
                                        min_count=2, multi=True, custom=True)
            difficulties_str = '\n - '.join(self._difficulties)
            print(f"Selected difficulties:\n - {difficulties_str}")
            # - flag
            self._flag_prefix = readline("Enter flag prefix", default=self._flag_prefix)
            self._flag_suffix = readline("Enter flag prefix", default=self._flag_suffix)
            # - domain
            self._domain = readline("Enter domain", default=self._domain)
            # - docker
            self._docker_user = readline("Enter docker user", default=self._docker_user)
            self._docker_registry = readline("Enter docker registry host", default=self._docker_registry)
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=2)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
