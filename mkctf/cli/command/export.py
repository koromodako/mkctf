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
    exported = [info for info in api.export(export_dir, args.tags, args.slug, args.include_disabled) if not 'ignored' in info]
    export_map = {info['slug']: str(info['archive_path']) for info in exported}
    app_log.info("creating export.map...")
    with export_dir.joinpath('export.map').open('w') as fp:
        dump(export_map, fp)
    app_log.info("done.")
    return exported

def setup_export(subparsers):
    parser = subparsers.add_parser('export', help="export public resources for each challenge.")
    parser.add_argument('export_dir', type=Path, help="folder where archives must be written. If the folder does not exist it will be created.")
    parser.add_argument('-t', '--tags', action='append', default=[], help="challenge's tags.")
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.add_argument('--include-disabled', action='store_true', help="export disabled challenges too.")
    parser.set_defaults(func=export)
