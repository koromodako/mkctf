"""logging helper
"""

from logging import basicConfig, getLogger

from rich.console import Console
from rich.logging import RichHandler

_HANDLER = RichHandler(
    console=Console(stderr=True),
    log_time_format='[%Y-%m-%dT%H:%M:%S]',
)
basicConfig(
    level='NOTSET',
    format='%(message)s',
    handlers=[],
)
LOGGER = getLogger('mkctf')
LOGGER.setLevel('INFO')
LOGGER.addHandler(_HANDLER)


def log_enable_debug(enable=True):
    """enable debug logging level"""
    LOGGER.setLevel('DEBUG' if enable else 'INFO')


def log_enable_logging(enable=True):
    """enable logging"""
    handlers = LOGGER.handlers
    if enable and _HANDLER not in handlers:
        LOGGER.addHandler(_HANDLER)
    elif not enable and _HANDLER in handlers:
        LOGGER.removeHandler(_HANDLER)
