'''
file: build.py
date: 2018-03-02
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
import mkctf.helper.cli as cli
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text, format_rcode2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def build(api, args):
    '''Builds one or more challenges
    '''
    if not args.yes and not cli.confirm('do you really want to build?'):
        return False

    timeout = args.timeout
    tags, slug = args.tags, args.slug

    sep = '-' * 35
    chall_sep = format_text(HSEP, 'blue', attrs=['bold'])
    exc_sep = format_text(f'{sep} [EXCEPT] {sep}', 'magenta')
    out_sep = format_text(f'{sep} [STDOUT] {sep}', 'blue')
    err_sep = format_text(f'{sep} [STDERR] {sep}', 'red')

    success = True
    async for challenge in api.build(tags):
        if slug is None or slug == challenge.slug:

            exception = None

            try:
                (code, stdout, stderr) = await challenge.build(timeout)
            except Exception as e:
                exception = e
                success = False
                code = -1

            if args.json:
                results.append({
                    'slug': challenge.slug,
                    'tags': challenge.tags,
                    'code': code,
                    'stdout': stdout,
                    'stderr': stderr,
                    'exception': exception
                })
            else:
                chall_description = f"{challenge.slug}{challenge.tags}"
                if not no_color:
                    chall_description = colored(chall_description, 'blue')

                chall_status = returncode2str(code, args.no_color)

                print(chall_sep)
                print(f"{chall_description} {chall_status}")

                if code < 0:
                    print(exc_sep)
                    print(exception)
                elif code > 0:
                    print(out_sep)
                    print(stdout.decode().strip())
                    print(err_sep)
                    print(stderr.decode().strip())

    return results if args.json else success
