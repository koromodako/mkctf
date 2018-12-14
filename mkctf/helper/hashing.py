'''
file: hashing.py
date: 2018-03-02
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from hashlib import sha256
# =============================================================================
#  FUNCTIONS
# =============================================================================
def hash_file(filepath):
    '''Hashes given file content using SHA256

    Arguments:
        filepath {Path} -- File's path

    Returns:
        str -- SHA256 hexadecimal digest
    '''
    h = sha256()

    with filepath.open('rb') as f:

        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)

    return h.hexdigest()
