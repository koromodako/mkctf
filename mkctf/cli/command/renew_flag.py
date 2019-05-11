# =============================================================================
#  FUNCTIONS
# =============================================================================
from mkctf.api import MKCTFAPI
from mkctf.cli import Answer, confirm
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def renew_flag(api, args):
    '''[summary]
    '''
    if not args.yes and confirm('do you really want to renew flags?') == Answer.NO:
        app_log.warning("operation cancelled by user.")
        return False
    renewed = [None for _ in api.renew_flag(tags=args.tags,
                                            categories=args.categories,
                                            slug=args.slug, size=args.size)]
    return renewed

def setup_renew_flag(subparsers):
    parser = subparsers.add_parser('renew-flag', help="renew flags. You might want to build and deploy/export after that.")
    parser.add_argument('-t', '--tag', dest='tags', action='append', default=[], help="challenge's tags. Can appear multiple times.")
    parser.add_argument('-c', '--category', dest='categories', action='append', default=[], help="challenge's category. Can appear multiple times.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.add_argument('--size', type=int, default=MKCTFAPI.FLAG_SIZE, help="flag's random string size (in bytes).")
    parser.set_defaults(func=renew_flag)
