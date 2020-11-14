# ==============================================================================
# IMPORTS
# ==============================================================================
from .configuration import Configuration

# ==============================================================================
# CLASSES
# ==============================================================================
class ChallengeConfiguration(Configuration):
    """[summary]"""

    TYPE = 'challenge'
    DEFINITION = {
        'name': (str,),
        'slug': (str,),
        'tags': (list,),
        'flag': (str,),
        'author': (str,),
        'points': (int,),
        'enabled': (bool,),
        'category': (str,),
        'logo_url': (str,),
        'difficulty': (str,),
        'static_url': (str,),
    }

    @property
    def name(self):
        return self['name']

    @property
    def slug(self):
        return self['slug']

    @property
    def tags(self):
        return self['tags']

    @property
    def flag(self):
        return self['flag']

    @property
    def author(self):
        return self['author']

    @property
    def points(self):
        return self['points']

    @property
    def enabled(self):
        return self['enabled']

    @property
    def category(self):
        return self['category']

    @property
    def logo_url(self):
        return self['logo_url']

    @property
    def difficulty(self):
        return self['difficulty']

    @property
    def static_url(self):
        return self['static_url']
