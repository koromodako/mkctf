# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import json
from datetime import datetime
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
class RepositoryConfigurationWizard:
    '''[summary]
    '''
    def __init__(self, default):
        self._name = f'Example CTF {datetime.now().year}'
        # - tags & difficulties
        self._tags = default['tags']
        self._difficulties = default['difficulties']
        # - flag
        self._flag_prefix = default['flag']['prefix']
        self._flag_suffix = default['flag']['suffix']
        # - domain
        self._domain = default['domain']
        # - docker
        self._docker_user = default['docker']['user']
        self._docker_registry = default['docker']['registry']

    @property
    def result(self):
        return {
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
                'base_url': f'https://static.{self.domain}/'
            },
            'standard': {
                'dirs': {
                    'public': ['public-files'],
                    'private': ['healthcheck'],
                },
                'build': {'name': 'build', 'from': 'build.jinja'},
                'deploy': {'name': 'deploy', 'from': 'deploy.jinja'},
                'healthcheck': {'name': 'healthcheck', 'from': 'healthcheck.jinja'},
                'description': {'name': 'description.md', 'from': 'description.md.jinja'},
                'files': [
                    {'name': '.gitignore'},
                    {'name': 'writeup.md', 'from': ''},
                    {'name': 'healthcheck/healthcheck.deps', 'from': 'healthcheck.deps'},
                ],
            },
            'categories': {
                'simple': {
                    'dirs': {
                        'public': [],
                        'private': ['private-files'],
                    },
                    'files': [],
                },
                'server': {
                    'dirs': {
                        'public': [],
                        'private': ['server-files'],
                    },
                    'files': [
                        {'name': 'server-files/Dockerfile', 'from': 'Dockerfile.server'},
                    ],
                },
                'sandbox': {
                    'dirs': {
                        'public': [],
                        'private': ['server-files'],
                    },
                    'files': [
                        {'name': 'server-files/Dockerfile', 'from': 'Dockerfile.sandbox-server'},
                        {'name': 'server-files/Dockerfile.sandbox', 'from': 'Dockerfile.server'},
                        {'name': 'server-files/banner', 'from': 'banner'},
                        {'name': 'server-files/sshd_config', 'from': 'sshd_config'},
                        {'name': 'server-files/sandbox_start.sh', 'exec': True, 'from': 'sandbox_start.sh.jinja'},
                    ],
                },
            },
        }

    def show(self):
        while True:
            self._name = readline(self._name, "Enter a name")
            # - tags & difficulties
            self._tags = choose(self._tags, "Choose tags or/and add some", min_count=2, multi=True, custom=True)
            self._difficulties = choose(self._difficulties, "Choose difficulties or/and add some",
                                        min_count=2, multi=True, custom=True)
            # - flag
            self._flag_prefix = readline(self._flag_prefix, "Enter flag prefix")
            self._flag_suffix = readline(self._flag_suffix, "Enter flag prefix")
            # - domain
            self._domain = readline(self._domain, "Enter domain")
            # - docker
            self._docker_user = readline(self._docker_user, "Enter docker user")
            self._docker_registry = readline(self._docker_registry, "Enter docker registry host")
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=2)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
