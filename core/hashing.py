# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: hashing.py
#     date: 2018-03-02
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from hashlib import sha256
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Hashes file content reading the file block per blocks
##
## @return     Hash hex digest
##
def hash_file(file_path):
    h = sha256()

    with open(file_path, 'rb') as f:

        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)

    return h.hexdigest()
