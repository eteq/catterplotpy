from __future__ import absolute_import, division, print_function, unicode_literals  # just in case, for py2 to be py3-ish

import numpy as np
import matplotlib

_CAT_DATA = np.load('data/cats.npy') # N x 72 x 72, 0 is transparent, 1 is full-cat
def _get_cat_num(i):
    return _CAT_DATA[i]

def _ncats():
    return len(_CAT_DATA)


def catter(*args, **kwargs):
    """
    Accepts all  ``scatter`` args, with added keyword argument ``cat`` which can
    be:
    * a number: the index of the cat symbol
    * 'rand' : random cats
    """
    kwargs.pop('cat', 'rand')
    raise NotImplementedError()
