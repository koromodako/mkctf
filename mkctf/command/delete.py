"""delete command
"""

from ..helper.cli import Answer, confirm
from ..helper.logging import LOGGER


async def delete(mkctf_api, args):
    """Deletes a challenge"""
    if (
        not args.yes
        and confirm("do you really want to run delete?") == Answer.NO
    ):
        LOGGER.warning("operation cancelled by user")
        return False
    deleted = mkctf_api.delete(args.slug)
    if deleted:
        LOGGER.info("%s deleted", args.slug)
    else:
        LOGGER.warning("operation failed")
    return deleted


def setup_delete(subparsers):
    """Setup delete command"""
    parser = subparsers.add_parser('delete', help="delete a challenge")
    parser.add_argument('slug', help="challenge's slug")
    parser.set_defaults(func=delete)
