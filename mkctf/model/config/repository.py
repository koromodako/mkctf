# ==============================================================================
# IMPORTS
# ==============================================================================
import os
from hashlib import sha1
from .configuration import Configuration
from mkctf.cli.wizards import RepositoryConfigurationWizard
# ==============================================================================
# CLASSES
# ==============================================================================
class RepositoryConfiguration(Configuration):
    '''[summary]
    '''
    def __init__(self, general_conf, path):
        '''[summary]
        '''
        super().__init__(path)
        self._general_conf = general_conf

    def load(self):
        super().load()
        exe = {'exec': True}
        self.raw['standard']['build'].update(exe)
        self.raw['standard']['deploy'].update(exe)
        self.raw['standard']['healthcheck'].update(exe)

    def update(self, override_conf=None):
        '''[summary]
        '''
        final_conf = override_conf
        if not final_conf:
            default_conf = self.raw or self._general_conf.raw
            wizard = RepositoryConfigurationWizard(default_conf)
            if not wizard.show():
                return
            final_conf = wizard.result
        self.override(final_conf)
        self.save()

    @property
    def tags(self):
        return self.raw['tags']

    @property
    def difficulties(self):
        return self.raw['difficulties']

    @property
    def categories(self):
        return list(self.raw['categories'].keys())

    @property
    def flag_prefix(self):
        return self.raw['flag']['prefix']

    @property
    def flag_suffix(self):
        return self.raw['flag']['suffix']

    @property
    def static_base_url(self):
        return self.raw['static']['base_url']

    @property
    def static_salt(self):
        return bytes.fromhex(self.raw['static']['salt'])

    @property
    def build(self):
        return self.raw['standard']['build']['name']

    @property
    def deploy(self):
        return self.raw['standard']['deploy']['name']

    @property
    def healthcheck(self):
        return self.raw['standard']['healthcheck']['name']

    @property
    def description(self):
        return self.raw['standard']['description']['name']

    def directories(self, category, public_only=False):
        dir_list = self.raw['standard']['dirs']['public']
        dir_list += self.raw['categories'][category]['dirs']['public']
        if not public_only:
            dir_list += self.raw['standard']['dirs']['private']
            dir_list += self.raw['categories'][category]['dirs']['private']
        return dir_list

    def files(self, category):
        file_list = [
            self.raw['standard']['build'],
            self.raw['standard']['deploy'],
            self.raw['standard']['healthcheck'],
            self.raw['standard']['description'],
        ]
        file_list += self.raw['standard']['files']
        file_list += self.raw['categories'][category]['files']
        return file_list

    def make_rand_flag(self, size=16):
        '''Generate a random flag
        '''
        return f"{self.flag_prefix}{os.urandom(size).hex()}{self.flag_suffix}"

    def make_static_url(self, slug):
        '''Generate a static url
        '''
        url = self.static_base_url
        if not url.endswith('/'):
            url += '/'
        url += f'{sha1(slug.encode() + self.static_salt).hexdigest()}.tar.gz'
        return url
