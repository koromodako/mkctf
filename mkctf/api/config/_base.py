"""Base configuration generic class
"""

from pathlib import Path

from ruamel.yaml import YAML

from ...helper.exception import MKCTFAPIException


class ConfigBase:
    """Configuration base class"""

    @classmethod
    def load(cls, filepath: Path):
        """Load and build a class from a YAML configuration"""
        if not filepath.is_file():
            return cls()
        try:
            conf = YAML(typ='safe').load(filepath)
            conf = cls.from_dict(conf)
        except Exception as exc:
            raise MKCTFAPIException("failed to load configuration") from exc
        return conf

    def dump(self, filepath: Path):
        """Serialize self to a file using YAML format"""
        yaml = YAML(typ='safe')
        yaml.default_flow_style = False
        with filepath.open('w') as fstream:
            fstream.write(
                "#\n"
                "# This file was generated using mkCTF utility.\n"
                "# Do not edit it manually unless you know exactly what you're doing.\n"
                "# Keep #PEBCAK in mind.\n"
                "#\n"
            )
            yaml.dump(self.to_dict(), fstream)

    @classmethod
    def from_dict(cls, dct):
        """Build instance from dict"""
        raise NotImplementedError

    def to_dict(self):
        """Build dict from instance"""
        raise NotImplementedError
