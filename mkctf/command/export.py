# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: export.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import tarfile
from mkctf.helper.hashing import hash_file
# =============================================================================
#  FUNCTIONS
# =============================================================================

def __export_chall(logger, export_dir, include_disabled, chall):
    """Exports one challenge

    Creates an archive containing all of the challenge "exportable" files.

    Arguments:
        logger {Logger} -- [description]
        export_dir {Path} -- [description]
        include_disabled {bool} -- [description]
        chall {Challenge} -- [description]

    Returns:
        bool -- True if function succeeded
    """
    if not chall.is_static():
        logger.warning("challenge ignored (not static): "
                       "{}/{}.".format(chall.category(),chall.slug()))
        return False

    if not include_disabled and not chall.enabled():
        logger.warning("challenge ignored (disabled): "
                       "{}/{}.".format(chall.category(),chall.slug()))
        return False

    logger.info("exporting {}/{}...".format(chall.category(),
                                            chall.slug()))

    archive_name = '{}.{}.tgz'.format(chall.category(), chall.slug())
    archive_path = export_dir.joinpath(archive_name)
    with tarfile.open(str(archive_path), 'w:gz') as arch:
        for entry in chall.exportable():
            arch.add(entry.path, arcname=entry.name)

    checksum_name = '{}.sha256'.format(archive_name)
    checksum_path = export_dir.joinpath(checksum_name)
    checksum_path.write_text('{}  {}\n'.format(hash_file(archive_path),
                                               archive_name))

    logger.info("done.")
    return True

async def export(args, repo, logger):
    """Exports one or more challenges

    Creates one archive per challenge in a given directory

    Arguments:
        args {Namespace} -- [description]
        repo {Repository} -- [description]
        logger {Logger} -- [description]
    """
    export_dir = args.export_dir.resolve()
    category, slug = args.category, args.slug
    include_disabled = args.include_disabled

    status = True

    if category is None and slug is not None:
        logger.error("you must specify --category if you use --chall-slug.")
        status = False
    else:
        export_dir.mkdir(parents=True, exist_ok=True)

        if slug is not None:
            chall = repo.find_chall(category, slug)

            if chall is None:
                logger.error("challenge not found: {}/{}".format(chall.category(),
                                                                 chall.slug()))
                status = False
            else:
                status = __export_chall(logger,
                                        export_dir,
                                        include_disabled,
                                        chall)
        else:
            for category, challenges in repo.scan(category):
                for chall in challenges:
                    if not __export_chall(logger,
                                          export_dir,
                                          include_disabled,
                                          chall):
                        status = False

    return {'status': status} if args.json else status
