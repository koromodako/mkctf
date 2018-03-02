# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: wrapper.py
#     date: 2018-03-01
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from functools import wraps
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Wraps a class method with this function to turn it into a lazy
##             getter.
##             Class member value will be computed on the first call to this
##             function and will never be computed again after that.
##
## @param      cls_member_name  Name of the member to use
##
def lazy(cls_member_name):

    def wrapper(f):

        @wraps(f)
        def wrapped(self, *args, **kwds):
            if not hasattr(self, cls_member_name):
                setattr(self, cls_member_name, f(self, *args, **kwds))

            return getattr(self, cls_member_name)

        return wrapped

    return wrapper
