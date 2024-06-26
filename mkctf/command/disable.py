"""disable command
"""

from ..helper.logging import LOGGER


async def disable(mkctf_api, args):
    """Enables a challenge"""
    disabled = mkctf_api.disable(args.slug)
    if disabled:
        LOGGER.info("%s disabled", args.slug)
    else:
        LOGGER.warning("operation failed")
    return disabled


def setup_disable(subparsers):
    """Setup disable command"""
    parser = subparsers.add_parser('disable', help="disable a challenge")
    parser.add_argument('slug', help="challenge's slug")
    parser.set_defaults(func=disable)
