# =============================================================================
#  FUNCTIONS
# =============================================================================
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def update_meta(api, args):
    '''[summary]
    '''
    updated = [None for _ in api.update_meta(tags=args.tags,
                                             categories=args.categories,
                                             slug=args.slug)]
    return updated

def setup_update_meta(subparsers):
    parser = subparsers.add_parser('update-meta', help="Update challenge metadata. You might want to run this command after reconfiguring the repository.")
    parser.add_argument('-t', '--tag', dest='tags', action='append', default=[], help="challenge's tags. Can appear multiple times.")
    parser.add_argument('-c', '--category', dest='categories', action='append', default=[], help="challenge's category. Can appear multiple times.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.set_defaults(func=update_meta)
