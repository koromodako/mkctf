# =============================================================================
#  IMPORTS
# =============================================================================
from json import dump
from pathlib import Path
from mkctf.helper.log import app_log
from mkctf.helper.formatting import TAB, HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def export(api, args):
    '''Exports one or more challenges

    Creates one archive per challenge in a given directory
    '''
    found = False
    export_dir = args.export_dir.resolve()
    exported = [info for info in api.export(export_dir, tags=args.tags, categories=args.categories,
                                            slug=args.slug, include_disabled=args.include_disabled)]
    export_map = {info['slug']: str(info['archive_path']) for info in exported}
    app_log.info("creating export.map...")
    with export_dir.joinpath('export.map').open('w') as fp:
        dump(export_map, fp)
    app_log.info("done.")
    return exported

def setup_export(subparsers):
    parser = subparsers.add_parser('export', help="export public resources for each challenge.")
    parser.add_argument('export_dir', type=Path, help="folder where archives must be written. If the folder does not exist it will be created.")
    parser.add_argument('-t', '--tag', action='append', default=[], dest='tags', metavar='TAG', help="tag of challenges to include. Can appear multiple times.")
    parser.add_argument('-c', '--category', action='append', default=[], dest='categories', metavar='CATEGORY', help="category of challenge to include. Can appear multiple times.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.add_argument('--include-disabled', action='store_true', help="export disabled challenges too.")
    parser.set_defaults(func=export)
