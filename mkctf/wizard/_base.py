"""Wizard generic interface
"""

from json import dumps

from ..api.config._base import ConfigBase
from ..helper.cli import Answer, confirm
from ..helper.logging import LOGGER


class WizardBase:
    """Interactive command line wizard"""

    def _interactive_form(self) -> type[ConfigBase]:
        raise NotImplementedError

    def show(self) -> type[ConfigBase]:
        """Show interactive form and loop if needed"""
        while True:
            # create config using interactive form
            try:
                config = self._interactive_form()
            except (KeyboardInterrupt, EOFError):
                print()
                return None
            # confirm, abort or retry
            answer = confirm(
                f"Are you ok with this configuration:\n{dumps(config.to_dict(), indent=2)}",
                abort=True,
            )
            if answer == Answer.YES:
                return config
            if answer == Answer.ABORT:
                LOGGER.warning("user canceled the operation.")
                return None
