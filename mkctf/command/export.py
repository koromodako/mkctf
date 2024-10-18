"""push command
"""

from json import dumps
from pathlib import Path

from ..helper.logging import LOGGER


async def export(mkctf_api, args):
    """Exports one or more challenges

    Creates one archive per challenge in a given directory
    """
    LOGGER.info("exporting challenges...")
    export_directory = args.export_directory.resolve()
    export_map = {
        slug: str(archive_path)
        for slug, archive_path in mkctf_api.export(
            export_directory,
            tags=args.tags,
            categories=args.categories,
            slug=args.slug,
            export_disabled=args.export_disabled,
        )
    }
    if not export_map:
        LOGGER.warning("export is empty")
        return False
    LOGGER.info("creating export.map...")
    (export_directory / 'export.map').write_text(dumps(export_map))
    LOGGER.info("export done")
    return True


def setup_export(subparsers):
    """Setup export command"""
    parser = subparsers.add_parser(
        'export', help="export public resources for each challenge"
    )
    parser.add_argument(
        'export_directory',
        type=Path,
        help="folder where archives must be written. If the folder does not exist it will be created",
    )
    parser.add_argument(
        '--tag',
        '-t',
        action='append',
        default=[],
        dest='tags',
        metavar='TAG',
        help="tag of challenges to include, can appear multiple times",
    )
    parser.add_argument(
        '--category',
        '-c',
        action='append',
        default=[],
        dest='categories',
        metavar='CATEGORY',
        help="category of challenge to include, can appear multiple times",
    )
    parser.add_argument('-s', '--slug', help="challenge's slug")
    parser.add_argument(
        '--export-disabled',
        action='store_true',
        help="also export disabled challenges",
    )
    parser.set_defaults(func=export)
