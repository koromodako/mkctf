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
    print("challenges:")
    for challenge in api.enum(args.tags, args.slug):
        slug, conf = challenge['slug'], challenge['conf']
        found = True
        if conf is None:
            app_log.error(f"configuration missing. Run `mkctf configure -s {slug}`")
            continue
        static = ' [STANDALONE]' if conf['standalone'] else ''
        chall_entry = f"{TAB}- {slug}{static}"
        color = 'green' if conf['enabled'] else 'red'
        chall_entry = format_text(chall_entry, color, attrs=['bold'])
        del conf['enabled']
        del conf['standalone']
        del conf['slug']
        description = challenge['description'] or format_text('empty description', 'red', attrs=['bold'])
        text = format_dict2str(conf)
        text += "\n+ description:"
        text += indent(f"\n{HSEP}\n{description}\n{HSEP}", TAB)
        print(chall_entry)
        print(indent(text[1:], TAB * 2))
    if not found:
        app_log.warning("no challenge found matching given constraints.")
    return found

def setup_enum(subparsers):
    parser = subparsers.add_parser('enum', help="enumerate challenges.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.set_defaults(func=enum)
