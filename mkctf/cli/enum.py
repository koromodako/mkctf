# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.helper.formatting import TAB, HSEP, format_text, format_dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enum(api, args):
    '''Enumerates challenges
    '''
    found = False
    print("challenges:")
    for slug, conf in api.enum(args.tags, args.slug)
        found = True
        if conf is None:
            app_log.error(f"configuration missing. Run `mkctf configure -s {challenge.slug}`")
            continue
        static = ' [STANDALONE]' if conf['standalone'] else ''
        chall_entry = f"{TAB}{TAB}- {challenge.slug}{static}"
        color = 'green' if conf['enabled'] else 'red'
        chall_entry = format_text(chall_entry, color, attrs=['bold'])
        del conf['enabled']
        del conf['standalone']
        del conf['slug']
        text = format_dict2str(conf).replace("\n", f"\n{TAB}{TAB}{TAB}")
        print(chall_entry)
        print(text[1:])
    if not found:
        app_log.warning("no challenge found matching given constraints.")
    return found

def setup_enum(subparsers):
    parser = subparsers.add_parser('enum', help="enumerate challenges.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.set_defaults(func=enum)
