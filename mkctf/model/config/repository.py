# ==============================================================================
# IMPORTS
# ==============================================================================
import os
from hashlib import sha1
from mkctf.exception import MKCTFAPIException
from .configuration import Configuration

# ==============================================================================
# CLASSES
# ==============================================================================
class RepositoryConfiguration(Configuration):
    """[summary]"""

    TYPE = 'repository'
    DEFINITION = {
        'name': (str,),
        'tags': (list,),
        'difficulties': (list,),
        'flag': {
            'prefix': (str,),
            'suffix': (str,),
        },
        'domain': (str,),
        'docker': {
            'user': (str,),
            'registry': (str,),
        },
        'static': {'salt': (str,), 'base_url': (str,)},
        'standard': {
            'dirs': {
                'public': (list,),
                'private': (list,),
            },
            'build': {'name': (str,)},
            'deploy': {'name': (str,)},
            'healthcheck': {'name': (str,)},
            'description': {'name': (str,)},
            'files': (list,),
        },
        'categories': {
            'simple': {
                'dirs': {
                    'public': (list,),
                    'private': (list,),
                },
                'files': (list,),
            },
            'server': {
                'dirs': {
                    'public': (list,),
                    'private': (list,),
                },
                'files': (list,),
            },
            'sandbox': {
                'dirs': {
                    'public': (list,),
                    'private': (list,),
                },
                'files': (list,),
            },
        },
    }

    @classmethod
    def load(cls, path):
        """Overrided load classmethod

        Ensure some specific files have exe mode set to True
        """
        conf = super(RepositoryConfiguration, cls).load(path)
        if conf.get('standard'):
            exe = {'exec': True}
            conf['standard']['build'].update(exe)
            conf['standard']['deploy'].update(exe)
            conf['standard']['healthcheck'].update(exe)
        return conf

    @property
    def name(self):
        return self['name']

    @property
    def tags(self):
        return self['tags']

    @property
    def difficulties(self):
        return self['difficulties']

    @property
    def categories(self):
        return list(self['categories'].keys())

    @property
    def flag_prefix(self):
        return self['flag']['prefix']

    @property
    def flag_suffix(self):
        return self['flag']['suffix']

    @property
    def domain(self):
        return self['domain']

    @property
    def docker_user(self):
        return self['docker']['user']

    @property
    def docker_registry(self):
        return self['docker']['registry']

    @property
    def static_base_url(self):
        return self['static']['base_url']

    @property
    def static_salt(self):
        return bytes.fromhex(self['static']['salt'])

    @property
    def build(self):
        return self['standard']['build']['name']

    @property
    def deploy(self):
        return self['standard']['deploy']['name']

    @property
    def healthcheck(self):
        return self['standard']['healthcheck']['name']

    @property
    def description(self):
        return self['standard']['description']['name']

    def directories(self, category, public_only=False):
        """List dirs of given category

        List public dirs only when public_only is set to True
        """
        dir_list = self['standard']['dirs']['public']
        dir_list += self['categories'][category]['dirs']['public']
        if not public_only:
            dir_list += self['standard']['dirs']['private']
            dir_list += self['categories'][category]['dirs']['private']
        return dir_list

    def files(self, category):
        """List files of given category"""
        file_list = [
            self['standard']['build'],
            self['standard']['deploy'],
            self['standard']['healthcheck'],
            self['standard']['description'],
        ]
        file_list += self['standard']['files']
        file_list += self['categories'][category]['files']
        return file_list

    def make_rand_flag(self, size=16):
        """Generate a random flag"""
        return f"{self.flag_prefix}{os.urandom(size).hex()}{self.flag_suffix}"

    def make_static_url(self, slug):
        """Generate a static url"""
        url = self.static_base_url
        if not url.endswith('/'):
            url += '/'
        url += f'{sha1(slug.encode() + self.static_salt).hexdigest()}.tar.gz'
        return url
