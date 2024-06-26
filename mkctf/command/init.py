"""init command
"""

from ..helper.logging import LOGGER


async def init(mkctf_api, _):
    """Initializes mkctf repository"""
    initialized, reason = mkctf_api.init()
    if initialized:
        LOGGER.info("mkctf repository initialized")
    else:
        LOGGER.warning("operation failed: %s", reason)
    return initialized


def setup_init(subparsers):
    """Setup init command"""
    parser = subparsers.add_parser('init', help="initialize mkctf repository")
    parser.set_defaults(func=init)
