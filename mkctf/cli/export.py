# =============================================================================
#  IMPORTS
# =============================================================================
import tarfile
from mkctf.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def export(api, args):
    '''Exports one or more challenges

    Creates one archive per challenge in a given directory
    '''
    found = False
    export_dir = args.export_dir.resolve()
    for exported in api.export(export_dir, args.tags, args.slug, args.include_disabled):
        found = True
        print(f"{format_text(exported['slug'], 'blue')} exported to:")
        print(f"{TAB}archive: {exported['archive_path']}")
        print(f"{TAB}checksum: {exported['checksum_path']}")
    return found

def setup_export(subparsers):
    parser = subparsers.add_parser('export', help="export enabled static challenges.")
    parser.add_argument('export_dir', type=Path, help="folder where archives must be written. If the folder does not exist it will be created.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.add_argument('--include-disabled', action='store_true', help="export disabled challenges too.")
    parser.set_defaults(func=export)
