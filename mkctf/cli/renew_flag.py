# =============================================================================
#  FUNCTIONS
# =============================================================================
import mkctf.helper.cli as cli
from mkctf.api import MKCTFAPI
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def renew_flag(api, args):
    '''[summary]
    '''
    if not args.yes and not cli.confirm('do you really want to renew flags?'):
        app_log.warning("operation cancelled by user.")
        return False
    for result in api.renew_flag(args.tags, args.slug, args.size):
        chall_desc = format_text(f"{result['slug']}", 'blue')
        print(f"{chall_desc} => {result['flag']}")
    return True

def setup_renew_flag(subparsers):
    parser = subparsers.add_parser('renew-flag', help="renew flags. You might want to build and deploy/export after that.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.add_argument('--size', type=int, default=MKCTFAPI.DEFAULT_FLAG_SIZE, help="flag's random string size (in bytes).")
    parser.set_defaults(func=renew_flag)
