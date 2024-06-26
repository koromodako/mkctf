"""enable command
"""

from ..helper.logging import LOGGER


async def enable(mkctf_api, args):
    """Enables a challenge"""
    enabled = mkctf_api.enable(args.slug)
    if enabled:
        LOGGER.info("%s enabled", args.slug)
    else:
        LOGGER.warning("operation failed")
    return enabled


def setup_enable(subparsers):
    """Setup enable command"""
    parser = subparsers.add_parser('enable', help="enable a challenge")
    parser.add_argument('slug', help="challenge's slug")
    parser.set_defaults(func=enable)
