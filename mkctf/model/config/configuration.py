# ==============================================================================
# IMPORTS
# ==============================================================================
from ruamel.yaml import YAML
from mkctf.exception import MKCTFAPIException
from mkctf.helper.log import app_log

# ==============================================================================
# CLASSES
# ==============================================================================
class MetaConfiguration(type):
    """[summary]"""

    ABSTRACT_CLASSES = {'Configuration'}
    EXPECTED_MEMBERS = {'TYPE', 'DEFINITION'}

    def __new__(cls, name, bases, dct):
        """[summary]"""
        ncls = super().__new__(cls, name, bases, dct)
        if name in MetaConfiguration.ABSTRACT_CLASSES:
            return ncls
        for member in MetaConfiguration.EXPECTED_MEMBERS:
            if not dct.get(member):
                raise AttributeError(
                    f"Missing '{member}' in MetaConfiguration subclass!"
                )
        return ncls


# pylint: disable=E1101


class Configuration(dict, metaclass=MetaConfiguration):
    """[summary]"""

    @classmethod
    def load(cls, path):
        """Load and build a class from a YAML configuration"""
        conf = cls()
        if path.is_file():
            try:
                app_log.debug(
                    "loading %s configuration from %s", cls.TYPE, path
                )
                conf = YAML(typ='safe').load(path)
                conf = cls(conf)
            except Exception as exc:
                app_log.exception(
                    "failed to load %s configuration from %s", cls.TYPE, path
                )
                raise MKCTFAPIException("configuration load failed.") from exc
        return conf

    @property
    def raw(self):
        return dict(self)

    def __dict_check(self, obj, expected_obj, chain=''):
        """Recursive diffing and type checking between two dicts"""
        if isinstance(expected_obj, dict) and isinstance(obj, dict):
            for ek, ev in expected_obj.items():
                v = obj.get(ek)
                chain += f'.{ek}'
                if v is None:
                    app_log.warning(
                        "invalid %s configuration - missing key: %s",
                        self.TYPE,
                        chain,
                    )
                    return False
                if not self.__dict_check(v, ev, chain):
                    return False
        elif isinstance(expected_obj, tuple):
            if not isinstance(obj, expected_obj):
                app_log.warning(
                    "invalid %s configuration - %s has invalid type: %s (%s)",
                    self.TYPE,
                    chain,
                    obj,
                    type(obj),
                )
                return False
        else:
            app_log.warning(
                "invalid %s configuration - %s should be a dict: %s",
                self.TYPE,
                chain,
                obj,
            )
            return False
        return True

    def validate(self, throw=True):
        """Determine if self is valid against expected_obj definition"""
        if not self.__dict_check(self, self.DEFINITION):
            if throw:
                raise MKCTFAPIException(
                    f"{self.TYPE} configuration is missing or invalid."
                )
            return False
        return True

    def save(self, path):
        """Serialize self to a file using YAML format"""
        yaml = YAML(typ='safe')
        yaml.default_flow_style = False
        with path.open('w') as fp:
            fp.write(
                "#\n"
                "# This file was generated using mkCTF utility.\n"
                "# Do not edit it manually unless you know exactly what you're doing.\n"
                "# Keep #PEBCAK in mind.\n"
                "#\n"
            )
            yaml.dump(self.raw, fp)
