"""create command
"""

from ..helper.logging import LOGGER


async def create(mkctf_api, _):
    """Creates a challenge"""
    created = mkctf_api.create()
    if created:
        LOGGER.info("challenge created")
    else:
        LOGGER.warning("operation failed")
    return created


def setup_create(subparsers):
    """Setup create command"""
    parser = subparsers.add_parser('create', help="create a challenge")
    parser.set_defaults(func=create)
