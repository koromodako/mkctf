'''
file: api.py
date: 2018-03-20
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from pathlib import Path
from slugify import slugify
from argparse import ArgumentParser, Namespace
from traceback import print_exc
from mkctf.helper.log import app_log
from mkctf.helper.config import load_config
from mkctf.command.init import init
from mkctf.command.show import show
from mkctf.command.build import build
from mkctf.command.deploy import deploy
from mkctf.command.status import status
from mkctf.command.create import create
from mkctf.command.delete import delete
from mkctf.command.enable import enable
from mkctf.command.export import export
from mkctf.command.disable import disable
from mkctf.command.configure import configure
from mkctf.command.renew_flag import renew_flag
from mkctf.object.repository import Repository
# =============================================================================
#  CONFIGURATION
# =============================================================================
DEFAULT_SIZE = 32
DEFAULT_TIMEOUT = 4 # seconds
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFAPI:
    '''Provides access to all functionalities programmatically
    '''
    @staticmethod
    def parse_args():
        '''Parse command line arguments

        Returns:
            Namespace -- [description]
        '''
        p = ArgumentParser(add_help=True,
                           description="Manage CTF challenges repository.")
        p.add_argument('-q', '--quiet', action='store_true',
                       help="decrease program verbosity")
        p.add_argument('-d', '--debug', action='store_true',
                       help="output debug messages")
        p.add_argument('--no-color', action='store_true',
                       help="disable colored output")
        p.add_argument('-r', '--repo-root', type=Path, default=Path.cwd(),
                       help="repository's root folder absolute path.")
        p.add_argument('-j', '--json', action='store_true',
                       help="json formatted output.")
        p.add_argument('-f', '--force', action='store_true',
                       help="do not ask for confirmation.")
        # -- add subparsers
        sps = p.add_subparsers(dest='command', metavar='COMMAND')
        sps.required = True
        # ---- init
        init_p = sps.add_parser('init', help="initializes mkctf repository.")
        init_p.set_defaults(func=init)
        # ---- show
        show_p = sps.add_parser('show', help="shows challenges.")
        show_p.add_argument('-c', '--category', help="challenge's category.")
        show_p.add_argument('-s', '--slug', help="challenge's slug.")
        show_p.set_defaults(func=show)
        # ---- create
        create_p = sps.add_parser('create', help="creates a challenge.")
        create_p.set_defaults(func=create)
        # ---- delete
        delete_p = sps.add_parser('delete', help="deletes a challenge.")
        delete_p.add_argument('category', help="challenge's category.")
        delete_p.add_argument('slug', help="challenge's slug.")
        delete_p.set_defaults(func=delete)
        # ---- configure
        configure_p = sps.add_parser('configure', help="edits repository's config "
                                                       "or challenge's config.")
        configure_p.add_argument('-c', '--category', help="challenge's category.")
        configure_p.add_argument('-s', '--slug', help="challenge's slug.")
        configure_p.set_defaults(func=configure)
        # ---- enable
        enable_p = sps.add_parser('enable', help="enables a challenge.")
        enable_p.add_argument('category', help="challenge's category.")
        enable_p.add_argument('slug', help="challenge's slug.")
        enable_p.set_defaults(func=enable)
        # ---- disable
        disable_p = sps.add_parser('disable', help="disables a challenge.")
        disable_p.add_argument('category', help="challenge's category.")
        disable_p.add_argument('slug', help="challenge's slug.")
        disable_p.set_defaults(func=disable)
        # ---- export
        export_p = sps.add_parser('export', help="exports enabled static "
                                                 "challenges.")
        export_p.add_argument('export_dir', type=Path,
                              help="folder where archives must be written. If "
                                   "the folder does not exist it will be "
                                   "created.")
        export_p.add_argument('-c', '--category', help="challenge's category.")
        export_p.add_argument('-s', '--slug', help="challenge's slug.")
        export_p.add_argument('--include-disabled', action='store_true',
                              help="export disabled challenges too.")
        export_p.set_defaults(func=export)
        # ---- renew-flag
        renew_flag_p = sps.add_parser('renew-flag',
                                       help="renews flags. You might want to "
                                            "build and deploy/export after that.")
        renew_flag_p.add_argument('-c', '--category', help="challenge's category.")
        renew_flag_p.add_argument('-s', '--slug', help="challenge's slug.")
        renew_flag_p.add_argument('--size', type=int, default=DEFAULT_SIZE,
                                  help="flag's random string size (in bytes).")
        renew_flag_p.set_defaults(func=renew_flag)
        # ---- build
        build_p = sps.add_parser('build',
                                 help="builds challenges. After building "
                                      "challenges you might want to deploy/export.")
        build_p.add_argument('-c', '--category', help="challenge's category.")
        build_p.add_argument('-s', '--slug', help="challenge's slug.")
        build_p.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT,
                             help="override default timeout for subprocesses.")
        build_p.set_defaults(func=build)
        # ---- deploy
        deploy_p = sps.add_parser('deploy', help="deploy challenges.")
        deploy_p.add_argument('-c', '--category', help="challenge's category.")
        deploy_p.add_argument('-s', '--slug', help="challenge's slug.")
        deploy_p.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT,
                              help="override default timeout for subprocesses.")
        deploy_p.set_defaults(func=deploy)
        # ---- status
        status_p = sps.add_parser('status', help="check deployed challenge's "
                                                 "status using exploit/exploit.")
        status_p.add_argument('-c', '--category', help="challenge's category.")
        status_p.add_argument('-s', '--slug', help="challenge's slug.")
        status_p.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT,
                              help="override default timeout for subprocesses.")
        status_p.set_defaults(func=status)

        args = p.parse_args()

        args.configuration = None

        return args

    def __init__(self, repo_root, out=None):
        '''Constructs a new instance

        Arguments:
            repo_root {Path} -- [description]
            debug {bool} -- [description]
            quiet {bool} -- [description]
            no_color {bool} -- [description]

        Keyword Arguments:
            out {IOBase} -- [description] (default: {None})
        '''
        self.repo_root = Path(repo_root)
        app_log.debug('repo_root: {}', self.repo_root)

        self.glob_conf_path = Path.home() / '.config/mkctf.yml'
        app_log.debug('glob_conf_path: {}', self.glob_conf_path)

        self.glob_conf = load_config(self.glob_conf_path)
        app_log.debug('glob_conf: {}', self.glob_conf)

        self.repo_conf_path = self.repo_root / self.glob_conf['files']['config']['repository']
        app_log.debug('repo_conf_path: {}', self.repo_conf_path)

        self.repo = Repository(self.repo_conf_path, self.glob_conf)

    async def perform(self, ns):
        '''Performs a comand using given Namespace ns

        Arguments:
            ns {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        app_log.info("mkctf starts...")
        app_log.debug("ns: {}", ns)

        if ns.command != 'init' and self.repo.get_conf() is None:
            app_log.critical("mkctf repository must be initialized first. Run `mkctf init` first.")

        try:
            # -----------------------------------------------------------------
            # 'result' content depending on json argument value:
            # if ns.json:
            #   result = dict or None
            # else:
            #   result = True or False
            # -----------------------------------------------------------------
            result = await ns.func(ns, self.repo)
        except Exception as e:
            print_exc()
            app_log.critical("Ouuuuupss.....:(")

        if result:
            app_log.info("mkctf ended successfully." )
        else:
            app_log.error("mkctf ended with errors.")

        return result

    def __ns(self, func):
        '''Creates a standard Namespace used by all functions of the API

        Arguments:
            func {function} -- [description]

        Returns:
            Namespace -- [description]
        '''
        ns = Namespace()
        ns.json = True
        ns.force = True
        ns.no_color = True
        ns.command = func.__name__
        ns.func = func
        return ns

    def init(self):
        '''API wrapper for 'init' command

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(init)
        # perform
        return self.perform(ns)

    def show(self):
        '''API wrapper for 'show' command

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(show)
        # perform
        return self.perform(ns)

    def create(self,
               category,
               name,
               flag,
               points,
               parameters={},
               enabled=False,
               standalone=True):
        '''API wrapper for 'create' command

        Arguments:
            category {str} -- [description]
            name {str} -- [description]
            flag {str} -- [description]
            points {int} -- [description]
            parameters {dict} -- [description]
            enabled {bool} -- [description]
            standalone {bool} -- [description]

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(create)
        # parameters
        ns.configuration = {
                'name': name,
                'slug': slugify(name),
                'flag': flag,
                'points': points,
                'enabled': enabled,
                'category': category,
                'parameters': parameters,
                'standalone': standalone
        }
        # perform
        return self.perform(ns)

    def delete(self, category=None, slug=None):
        '''API wrapper for 'delete' command

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(delete)
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)

    def configure(self, configuration, category=None, slug=None):
        '''API wrapper for 'configure' command

        Arguments:
            configuration {dict} -- [description]

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(enable)
        # parameters
        ns.configuration = configuration
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)

    def enable(self, category, slug):
        '''API wrapper for 'enable' command

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(enable)
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)

    def disable(self, category, slug):
        '''API wrapper for 'disable' command

        Arguments:
            category {str} -- [description]
            slug {str} -- [description]

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(disable)
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)

    def export(self, export_dir,
               category=None, slug=None,
               include_disabled=False):
        '''API wrapper for 'export' command

        Arguments:
            export_dir {Path} -- [description]

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})
            include_disabled {bool} -- [description] (default: {False})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(export)
        # parameters
        ns.export_dir = export_dir
        ns.category = category
        ns.slug = slug
        ns.include_disabled = include_disabled
        # perform
        return self.perform(ns)

    def renew_flag(self, category=None, slug=None, size=DEFAULT_SIZE):
        '''API wrapper for 'renew_flag' command

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})
            size {int} -- [description] (default: {DEFAULT_SIZE})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(renew_flag)
        # parameters
        ns.category = category
        ns.slug = slug
        ns.size = size
        # perform
        return self.perform(ns)

    def build(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'build' command

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})
            timeout {int} -- [description] (default: {DEFAULT_TIMEOUT})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(build)
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)

    def deploy(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'deploy' command

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})
            timeout {int} -- [description] (default: {DEFAULT_TIMEOUT})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(deploy)
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)

    def status(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        '''API wrapper for 'status' command

        Keyword Arguments:
            category {str} -- [description] (default: {None})
            slug {str} -- [description] (default: {None})
            timeout {int} -- [description] (default: {DEFAULT_TIMEOUT})

        Returns:
            [type] -- [description]
        '''
        ns = self.__ns(status)
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)
