# ==============================================================================
# IMPORTS
# ==============================================================================
from .configuration import Configuration
from mkctf.cli.wizards import ChallengeConfigurationWizard
# ==============================================================================
# CLASSES
# ==============================================================================
class ChallengeConfiguration(Configuration):
    '''[summary]
    '''
    def __init__(self, repo_conf, path):
        '''[summary]
        '''
        super().__init__(path)
        self._repo_conf = repo_conf

    def update(self, override_conf=None):
        '''[summary]
        '''
        final_conf = override_conf
        if not final_conf:
            default_conf = self.raw or self._general_conf.raw
            wizard = ChallengeConfigurationWizard(default_conf)
            if not wizard.show():
                return
            final_conf = wizard.result
        self.override(final_conf)
        self.save()

    def enable(self, enabled):
        self.raw['enabled'] = enabled
        self.save()

    def renaw_flag(self, size):
        flag = self._repo_conf.make_rand_flag(size)
        self.raw['flag'] = flag
        self.save()
        return flag

    def update_static_url(self):
        static_url = self._repo_conf.make_static_url(self.slug)
        self.raw['static_url'] = static_url
        self.save()
        return static_url

    @property
    def name(self):
        return self.raw['name']

    @property
    def slug(self):
        return self.raw['slug']

    @property
    def enabled(self):
        return self.raw['enabled']

    @property
    def tags(self):
        return self.raw['tags']

    @property
    def category(self):
        return self.raw['category']

    @property
    def difficulty(self):
        return self.raw['difficulty']
