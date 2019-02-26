'''
file: export.py
date: 2018-03-02
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
import tarfile
from mkctf.helper.log import app_log
from mkctf.helper.hashing import hash_file
# =============================================================================
#  FUNCTIONS
# =============================================================================
def __export_chall(export_dir, include_disabled, chall):
    '''Exports one challenge

    Creates an archive containing all of the challenge "exportable" files.
    '''
    if not chall.is_standalone:
        app_log.warning(f"challenge ignored (not standalone): {chall.slug}.")
        return False

    if not include_disabled and not chall.enabled:
        app_log.warning(f"challenge ignored (disabled): {chall.slug}.")
        return False

    app_log.info(f"exporting {chall.slug}...")

    archive_name = f'{chall.slug}.tgz'
    archive_path = export_dir.joinpath(archive_name)
    with tarfile.open(str(archive_path), 'w:gz') as arch:
        for entry in chall.exportable():
            arch.add(entry.path, arcname=entry.name)

    checksum_name = f'{archive_name}.sha256'
    checksum_path = export_dir.joinpath(checksum_name)
    archive_hash = hash_file(archive_path)
    checksum_path.write_text(f'{archive_hash}  {archive_name}\n')

    app_log.info("done.")
    return True

async def export(args, repo):
    '''Exports one or more challenges

    Creates one archive per challenge in a given directory
    '''
    export_dir = args.export_dir.resolve()
    tags, slug = args.tags, args.slug
    include_disabled = args.include_disabled

    status = True
    export_dir.mkdir(parents=True, exist_ok=True)

    if slug is not None:
        chall = repo.find_chall(slug)

        if chall is None:
            app_log.error(f"challenge not found: {chall.slug}")
            status = False
        else:
            status = __export_chall(export_dir, include_disabled, chall)
    else:
        for chall in repo.scan(tags):
            if not __export_chall(export_dir, include_disabled, chall):
                status = False

    return {'status': status} if args.json else status
