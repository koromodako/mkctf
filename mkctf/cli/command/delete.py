# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.cli import Answer, confirm
from mkctf.helper.log import app_log

# =============================================================================
#  FUNCTIONS
# =============================================================================
async def delete(api, args):
    """Deletes a challenge"""
    if (
        not args.yes
        and confirm("do you really want to run delete?") == Answer.NO
    ):
        app_log.warning("operation cancelled by user.")
        return False
    result = api.delete(args.slug)
    return result['deleted']


def setup_delete(subparsers):
    parser = subparsers.add_parser('delete', help="delete a challenge.")
    parser.add_argument('slug', help="challenge's slug.")
    parser.set_defaults(func=delete)
