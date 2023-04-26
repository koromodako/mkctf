"""Wizard generic interface
"""
import typing as t
from json import dumps
from ..helper.cli import Answer, confirm
from ..helper.logging import LOGGER
from ..api.config._base import ConfigBase


class WizardBase:
    def _interactive_form(self) -> t.Type[ConfigBase]:
        raise NotImplementedError

    def show(self) -> t.Type[ConfigBase]:
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
