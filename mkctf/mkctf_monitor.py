#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from os import getenv
from signal import SIGINT, SIGTERM
from getpass import getpass
from asyncio import get_event_loop
from mkctf import __version__
from mkctf.api import MKCTFAPI, MKCTFAPIException
from mkctf.helper.log import app_log
from mkctf.monitoring import MKCTFMonitor
from mkctf.helper.argument_parser import MKCTFArgumentParser
# =============================================================================
#  GLOBALS
# =============================================================================
BANNER = r"""
           _     ____ _____ _____   __  __             _ _
 _ __ ___ | | __/ ___|_   _|  ___| |  \/  | ___  _ __ (_) |_ ___  _ __
| '_ ` _ \| |/ / |     | | | |_    | |\/| |/ _ \| '_ \| | __/ _ \| '__|
| | | | | |   <| |___  | | |  _|   | |  | | (_) | | | | | || (_) | |
|_| |_| |_|_|\_\\____| |_| |_|     |_|  |_|\___/|_| |_|_|\__\___/|_|   v{}

""".format(__version__)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''Parse command line arguments
    '''
    parser = MKCTFArgumentParser(BANNER, "A tool to monitor CTF challenges running cron-like healchecks")
    # -- add arguments
    parser.add_argument('--host', default=getenv('MKCTF_SB_HOST', 'scoreboard.ctf.insecurity-insa.fr'), help="scoreboard host, overrides MKCTF_SB_HOST (env)")
    parser.add_argument('--port', default=getenv('MKCTF_SB_PORT', 443), type=int, help="scoreboard port, overrides MKCTF_SB_PORT (env)")
    parser.add_argument('--username', '-u', default=getenv('MKCTF_SB_USER'), help="scoreboard username, overrides MKCTF_SB_USER (env)")
    parser.add_argument('--password', '-p', default=getenv('MKCTF_SB_PSWD'), help="scoreboard password, overrides MKCTF_SB_PSWD (env). Using this option is strongly discouraged.")
    parser.add_argument('--iter-cnt', default=-1, type=int, help="how many times should each task be executed, -1 means infinite.")
    parser.add_argument('--iter-delay', default=600, type=int, help="the interval between two starts of the same task (in seconds).")
    parser.add_argument('--task-timeout', default=480, type=int, help="the timeout for task execution (in seconds).")
    parser.add_argument('--worker-cnt', default=4, type=int, help="the count of workers to be spawned.")
    parser.add_argument('--post-timeout', default=60, type=int, help="the timeout for posting report to the scoreboard (in seconds).")
    parser.add_argument('--no-verify-ssl', action='store_true', help="disable SSL checks. Using this option is strongly discouraged.")
    # -- parse args and pre-process if needed
    return parser.parse_args()

def sigint_handler():
    '''Handles user interrupt signal
    '''
    app_log.warning("\nOuch... you just killed me... (x_x)")
    loop = get_event_loop()
    loop.stop()
    loop.close()

async def main():
    '''Main function
    '''
    args = parse_args()
    args.username = args.username or input("Scoreboard username: ")
    args.password = args.password or getpass("Scoreboard password: ")
    try:
        api = MKCTFAPI(args.repo_dir)
        monitor = MKCTFMonitor(api, args.host, args.port, args.username, args.password,
                               iter_cnt=-1, iter_delay=600,
                               task_timeout=120, worker_cnt=4,
                               post_timeout=60, no_verify_ssl=False)
        await monitor.run()
    except MKCTFAPIException as exc:
        app_log.critical(f"critical error: {exc.args[0]}")
        rcode = 1
    except:
        app_log.exception("Ouch... unhandled exception... (>_<)")
        rcode = 2
    return rcode

def app():
    '''mkctf-cli script entry point
    '''
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, sigint_handler)
    loop.add_signal_handler(SIGTERM, sigint_handler)
    rcode = loop.run_until_complete(main())
    loop.close()
    return rcode
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    exit(app())
