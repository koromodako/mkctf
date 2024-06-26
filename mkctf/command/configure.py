"""configure command
"""

from ..helper.logging import LOGGER


async def configure(mkctf_api, args):
    """Configures mkctf repository or a specific challenge"""
    configured = mkctf_api.configure(slug=args.slug)
    if configured:
        LOGGER.info("%s configured", args.slug)
    else:
        LOGGER.warning("operation failed")
    return configured


def setup_configure(subparsers):
    """Setup configure command"""
    parser = subparsers.add_parser(
        'configure', help="edit repository's config or challenge's config"
    )
    parser.add_argument('-s', '--slug', help="challenge's slug")
    parser.set_defaults(func=configure)
