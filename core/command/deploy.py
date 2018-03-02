# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: deploy.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
# =============================================================================
#  FUNCTIONS
# =============================================================================
def deploy(args, repo, logger):
    if not repo.cli.confirm('do you really want to deploy?'):
        return True

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

    for cat, challenges in repo.scan(category):
        for challenge in challenges:
            if slug is None or slug == challenge.slug():
                try:
                    exception = None
                    (status, code, stdout, stderr) = challenge.deploy(timeout)

                    if status is None and code is None:
                        s_str = 'TIMED OUT'
                        s_color = 'magenta'
                    elif status:
                        s_str = 'SUCCESS'
                        s_color = 'green'
                    else:
                        s_str = 'FAILURE'
                        s_color = 'red'

                    s_str += ' (code={})'.format(code)
                except Exception as e:
                    exception = e
                    status  = True
                    s_str = 'EXCEPTION'
                    s_color = 'magenta'

                if not args.no_color:
                    s_str = colored(s_str, s_color, attrs=['bold'])

                chall_desc = "[{}] -> {}".format(challenge.category(),
                                                 challenge.slug())
                if not no_color:
                    chall_desc = colored(chall_desc, 'blue')

                print(chall_sep)
                print("{} {}".format(chall_desc, s_str))

                if exception is not None:
                    print(exc_sep)
                    print(exception)
                elif not status:
                    print(out_sep)
                    print(stdout.decode().strip())
                    print(err_sep)
                    print(stderr.decode().strip())
