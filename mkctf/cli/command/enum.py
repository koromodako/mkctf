# =============================================================================
#  IMPORTS
# =============================================================================
from textwrap import indent, wrap
from mkctf.helper.log import app_log
from mkctf.helper.formatting import TAB, HSEP, format_text, format_dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enum(api, args):
    '''Enumerates challenges
    '''
    found = False
    for challenge in api.enum(tags=args.tags, categories=args.categories, slug=args.slug):
        slug, conf = challenge['slug'], challenge['conf']
        if not found:
            found = True
            print("challenges:")
        if conf is None:
            app_log.error(f"configuration missing. Run `mkctf configure -s {slug}`")
            continue
        chall_entry = f"{TAB}- {slug} [{conf['category'].upper()}]"
        color = 'green' if conf['enabled'] else 'red'
        chall_entry = format_text(chall_entry, color, attrs=['bold'])
        del conf['slug']
        del conf['enabled']
        del conf['category']
        description = challenge['description'] or format_text('empty description', 'red', attrs=['bold'])
        chall_details = format_dict2str(conf)
        chall_details += "\n+ description:"
        chall_details += indent(f"\n{HSEP}\n{description}\n{HSEP}", TAB)
        print(chall_entry)
        if not args.summarize:
            print(indent(chall_details[1:], TAB * 2))
    if not found:
        app_log.warning("no challenge found.")
    return found

def setup_enum(subparsers):
    parser = subparsers.add_parser('enum', help="enumerate challenges.")
    parser.add_argument('--summarize', action='store_true', help="Print a list of challenges without details.")
    parser.add_argument('-t', '--tag', action='append', default=[], dest='tags', metavar='TAG', help="tag of challenges to include. Can appear multiple times.")
    parser.add_argument('-c', '--category', action='append', default=[], dest='categories', metavar='CATEGORY', help="category of challenge to include. Can appear multiple times.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.set_defaults(func=enum)
