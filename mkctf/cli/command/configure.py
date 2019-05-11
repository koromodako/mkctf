# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def configure(api, args):
    '''Configures mkctf repository or a specific challenge
    '''
    result = api.configure(slug=args.slug)
    return result['configured']

def setup_configure(subparsers):
    parser = subparsers.add_parser('configure', help="edit repository's config or challenge's config.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.set_defaults(func=configure)
