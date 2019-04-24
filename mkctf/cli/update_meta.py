# =============================================================================
#  FUNCTIONS
# =============================================================================
import mkctf.helper.cli as cli
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def update_meta(api, args):
    '''[summary]
    '''
    updated = [None for _ in api.update_meta(args.tags, args.slug)]
    return updated

def setup_update_meta(subparsers):
    parser = subparsers.add_parser('update-meta', help="Update challenge metadata. You might want to run this command after reconfiguring the repository.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.set_defaults(func=update_meta)
