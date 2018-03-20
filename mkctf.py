# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: mkctf.py
#     date: 2018-03-20
#   author: paul.dautry
#  purpose:
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from os import getcwd
from pathlib import Path
from argparse import ArgumentParser, Namespace
from traceback import print_exc
from core.logger import Logger
from core.config import load_config
from core.command.init import init
from core.command.show import show
from core.command.build import build
from core.command.deploy import deploy
from core.command.status import status
from core.command.create import create
from core.command.delete import delete
from core.command.enable import enable
from core.command.export import export
from core.command.disable import disable
from core.command.configure import configure
from core.command.renew_flag import renew_flag
from core.object.repository import Repository
# =============================================================================
#  CONFIGURATION
# =============================================================================
DEFAULT_SIZE = 32
DEFAULT_TIMEOUT = 4 # seconds
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for mkctf API.
##
class MKCTFAPI:
    ##
    ## @brief      Parses commandline arguments
    ##
    @staticmethod
    def parse_args():
        p = ArgumentParser(add_help=True,
                           description="Manage CTF challenges repository.")
        p.add_argument('-q', '--quiet', action='store_true',
                       help="decrease program verbosity")
        p.add_argument('-d', '--debug', action='store_true',
                       help="output debug messages")
        p.add_argument('--no-color', action='store_true',
                       help="disable colored output")
        p.add_argument('-r', '--repo-root', default=getcwd(),
                       help="repository's root folder absolute path.")
        p.add_argument('-j', '--json', action='store_true',
                       help="json formatted output.")
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
        delete_p.add_argument('-c', '--category', help="challenge's category.")
        delete_p.add_argument('-s', '--slug', help="challenge's slug.")
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
        export_p.add_argument('export_dir', help="folder where archives must be "
                                                 "written. If the folder does not "
                                                 "exist it will be created.")
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
    ##
    ## @brief      Constructs the object.
    ##
    def __init__(self, repo_root,
                 debug, quiet, no_color,
                 out=None):

        super(MKCTFAPI, self).__init__()
        self.logger = Logger(debug, quiet, no_color, out)

        self.repo_root = Path(repo_root)
        self.logger.debug('repo_root: {}'.format(self.repo_root))

        self.glob_conf_path = Path.home() / '.config/mkctf.yml'
        self.logger.debug('glob_conf_path: {}'.format(self.glob_conf_path))

        self.glob_conf = load_config(str(self.glob_conf_path))
        self.logger.debug('glob_conf: {}'.format(self.glob_conf))

        self.repo_conf_path = str(self.repo_root / self.glob_conf['files']['config']['repository'])
        self.logger.debug('repo_conf_path: {}'.format(self.repo_conf_path))

        self.repo = Repository(self.logger, self.repo_conf_path, self.glob_conf)
    ##
    ## @brief      { function_description }
    ##
    def perform(self, ns):
        if ns.command != 'init' and self.repo.get_conf() is None:
            logger.fatal("mkctf repository must be initialized first. Run "
                         "`mkctf init`.")

        try:
            # -----------------------------------------------------------------
            # 'result' content depending on json argument value:
            # if ns.json:
            #   result = dict or None
            # else:
            #   result = True or False
            # -----------------------------------------------------------------
            result = ns.func(ns, self.repo, self.logger)
        except Exception as e:
            print_exc()
            self.logger.fatal("Ouuuuupss.....:(")

        if result:
            self.logger.info("mkctf ended successfully." )
        else:
            self.logger.error("mkctf ended with errors.")

        return result
    ##
    ## @brief      { function_description }
    ##
    def init(self):
        ns = Namespace()
        ns.json = True
        ns.command = 'init'
        ns.func = init
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def show(self):
        ns = Namespace()
        ns.json = True
        ns.command = 'show'
        ns.func = show
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def create(self, configuration):
        ns = Namespace()
        ns.json = True
        ns.command = 'create'
        ns.func = create
        # parameters
        ns.configuration = configuration
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def delete(self, category=None, slug=None):
        ns = Namespace()
        ns.json = True
        ns.command = 'delete'
        ns.func = delete
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def configure(self, configuration, category=None, slug=None):
        ns = Namespace()
        ns.json = True
        ns.command = 'configure'
        ns.func = enable
        # parameters
        ns.configuration = configuration
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def enable(self, category, slug):
        ns = Namespace()
        ns.json = True
        ns.command = 'enable'
        ns.func = enable
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def disable(self, category, slug):
        ns = Namespace()
        ns.json = True
        ns.command = 'disable'
        ns.func = disable
        # parameters
        ns.category = category
        ns.slug = slug
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def export(self, export_dir,
               category=None, slug=None,
               include_disabled=False):
        ns = Namespace()
        ns.json = True
        ns.command = 'export'
        ns.func = export
        # parameters
        ns.export_dir = export_dir
        ns.category = category
        ns.slug = slug
        ns.include_disabled = include_disabled
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def renew_flag(self, category=None, slug=None, size=DEFAULT_SIZE):
        ns = Namespace()
        ns.json = True
        ns.command = 'renew_flag'
        ns.func = renew_flag
        # parameters
        ns.category = category
        ns.slug = slug
        ns.size = size
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def build(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        ns = Namespace()
        ns.json = True
        ns.command = 'build'
        ns.func = build
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def deploy(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        ns = Namespace()
        ns.json = True
        ns.command = 'deploy'
        ns.func = deploy
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)
    ##
    ## @brief      { function_description }
    ##
    def status(self, category=None, slug=None, timeout=DEFAULT_TIMEOUT):
        ns = Namespace()
        ns.json = True
        ns.command = 'status'
        ns.func = status
        # parameters
        ns.category = category
        ns.slug = slug
        ns.timeout = timeout
        # perform
        return self.perform(ns)
