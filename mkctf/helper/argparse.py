"""mkctf custom argument parser
"""

from pathlib import Path

from .logging import LOGGER, log_enable_debug, log_enable_logging


def generic_add_arguments(parser):
    parser.add_argument(
        '--quiet', '-q', action='store_true', help="disable logging"
    )
    parser.add_argument(
        '--debug', '-d', action='store_true', help="enable debug messages"
    )
    parser.add_argument(
        '--repository-directory',
        '-r',
        type=Path,
        default=Path.cwd(),
        help="absolute path of a mkCTF repository directory",
    )


def generic_parse_args(parser):
    """Print the banner, parse arguments and configure some helpers using generic arguments"""
    args = parser.parse_args()
    log_enable_debug(args.debug)
    log_enable_logging(not args.quiet)
    LOGGER.debug(args)
    return args
