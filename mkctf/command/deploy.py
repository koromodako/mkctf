'''
file: deploy.py
date: 2018-03-02
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
from mkctf.helper.formatting import returncode2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def deploy(args, repo):
    '''Deploys one or more challenges

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]

    Returns:
        [type] -- [description]
    '''
    if not args.force and not repo.cli.confirm('do you really want to deploy?'):
        return {'status': True} if args.json else True

    no_color, timeout = args.no_color, args.timeout
    category, slug = args.category, args.slug

    chall_sep = '=' * 80
    sep = '-' * 35
    exc_sep = '{sep} [EXCEPT] {sep}'.format(sep=sep)
    out_sep = '{sep} [STDOUT] {sep}'.format(sep=sep)
    err_sep = '{sep} [STDERR] {sep}'.format(sep=sep)

    if not no_color:
        chall_sep = colored(chall_sep, 'blue', attrs=['bold'])
        exc_sep = colored(exc_sep, 'magenta')
        out_sep = colored(out_sep, 'blue')
        err_sep = colored(err_sep, 'red')

    success = True
    results = []

    for cat, challenges in repo.scan(category):
        for challenge in challenges:
            if slug is None or slug == challenge.slug():

                exception = None

                try:
                    (code, stdout, stderr) = await challenge.deploy(timeout)
                except Exception as e:
                    exception = e
                    success = False
                    code = -1

                if args.json:
                    results.append({
                        'slug': challenge.slug(),
                        'category': challenge.category(),
                        'code': code,
                        'stdout': stdout,
                        'stderr': stderr,
                        'exception': exception
                    })
                else:
                    chall_description = "[{}] -> {}".format(challenge.category(),
                                                            challenge.slug())
                    if not no_color:
                        chall_description = colored(chall_description, 'blue')

                    chall_status = returncode2str(code, args.no_color)

                    print(chall_sep)
                    print("{} {}".format(chall_description, chall_status))

                    if code < 0:
                        print(exc_sep)
                        print(exception)
                    elif code > 0:
                        print(out_sep)
                        print(stdout.decode().strip())
                        print(err_sep)
                        print(stderr.decode().strip())

    return results if args.json else success
