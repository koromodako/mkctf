# =============================================================================
#  IMPORTS
# =============================================================================
from mkctf.api import MKCTFAPI
from mkctf.cli import Answer, confirm
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def healthcheck(api, args):
    '''Perform a healthcheck of at least one challenge
    '''
    if not args.yes and confirm('do you really want to perform a healthcheck?') == Answer.NO:
        app_log.warning("operation cancelled by user.")
        return False
    err_sep = format_text(f'{HSEP[:35]} [STDERR] {HSEP[:35]}', 'red')
    out_sep = format_text(f'{HSEP[:35]} [STDOUT] {HSEP[:35]}', 'blue')
    exc_sep = format_text(f'{HSEP[:35]} [EXCEPT] {HSEP[:35]}', 'magenta')
    chall_sep = format_text(HSEP, 'blue', attrs=['bold'])
    success = True
    async for build_result in api.healthcheck(tags=args.tags, categories=args.categories,
                                              slug=args.slug, dev=args.dev, timeout=args.timeout):
        rcode = build_result['rcode']
        chall_desc = format_text(f"{build_result['slug']}", 'blue')
        chall_health = api.rcode2health_str(rcode)
        print(chall_sep)
        print(f"{chall_desc} {chall_health}")
        if rcode < 0:
            success = False
            print(exc_sep)
            print(build_result['exception'])
        elif rcode > 0:
            print(out_sep)
            print(build_result['stdout'].decode().strip())
            print(err_sep)
            print(build_result['stderr'].decode().strip())
    return success

def setup_healthcheck(subparsers):
    parser = subparsers.add_parser('healthcheck', help="perform a healthcheck on a challenge using healthcheck script.")
    parser.add_argument('--dev', action='store_true', help="Runs the script in development mode.")
    parser.add_argument('-t', '--tag', action='append', default=[], dest='tags', metavar='TAG', help="tag of challenges to include. Can appear multiple times.")
    parser.add_argument('-c', '--category', action='append', default=[], dest='categories', metavar='CATEGORY', help="category of challenge to include. Can appear multiple times.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.add_argument('--timeout', type=int, default=MKCTFAPI.EXEC_TIMEOUT, help="override default timeout for subprocesses.")
    parser.set_defaults(func=healthcheck)
