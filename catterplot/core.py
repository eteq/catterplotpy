# Copyright 2017 Erik Tollerud
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function, unicode_literals  # just in case, for py2 to be py3-ish
import pkgutil, io

import numpy as np

from matplotlib import image, cm
from matplotlib import pyplot as plt



__all__ = ['get_cat_num', 'n_cats', 'catter']


 # N_cats x 72 x 72, 0 is transparent, 1 is full-cat
_CAT_DATA = np.load(io.BytesIO(pkgutil.get_data('catterplot', 'data/cats.npy')))

def get_cat_num(i):
    return _CAT_DATA[i]

def n_cats():
    return len(_CAT_DATA)


def catter(x, y, s=40, c=None, cat='random', alpha=1, ax=None, cmap=None,
           aspects='auto'):
    """
    A catter plot (scatter plot with cats).  Most arguments are interpreted
    the same as the matplotlib `scatter` function, except that ``s`` is the
    *data* size of the symbol (not pixel).  Additional kwargs include:

    ``cat`` can be:
    * int : the index of the cat symbol to use - you can use
      ``catterplot.n_cats()`` to get the number of cats available
    * a squence of ints : must match the data, but otherwise interpreted as for
      a scalar
    * 'random'/'rand' : random cats

    ``ax`` can be:
    * None: use the current default (pyplot) axes
    * an `Axes` : random cats

    ``aspects`` can be:
    * 'auto': the cats length-to-width is set to be square given the spread of
      inputs
    * a float: the height/width of the cats.  If not 1, ``s`` is interpreted as
      the geometric mean of the sizes
    * a sequence of floats: much match data, gives height/width
    """
    if ax is None:
        ax = plt.gca()

    if c is not None:
        if cmap is None:
            cmap = plt.rcParams['image.cmap']
        smap = cm.ScalarMappable(cmap=cmap)
        rgba = smap.to_rgba(c)
    else:
        rgba = np.ones((len(x), 4))
    rgba[:, 3] *= alpha

    if np.isscalar(s) or s.shape==tuple():
        s = np.ones(len(x))*s
    # otherwise assume shapes match

    if cat in ('rand', 'random'):
        cats = np.random.randint(n_cats(), size=len(x))
    else:
        try:
            cats = np.ones(len(x)) * cat
        except TypeError as e:
            raise TypeError('`cat` argument needs to be "random", a scalar, or match the input.', e)

    if aspects == 'auto':
        aspects = np.ptp(y)/np.ptp(x)
    if np.isscalar(aspects) or aspects.shape==tuple():
        aspects = np.ones(len(x)) * aspects

    ims = []
    for xi, yi, si, ci, cati, aspecti in zip(x, y, s, rgba, cats, aspects):
        data = get_cat_num(cati)

        offsetx = si * aspecti**-0.5 / (2 * data.shape[0])
        offsety = si * aspecti**0.5 / (2 * data.shape[1])

        im = image.AxesImage(ax, extent=(xi - offsetx, xi + offsetx,
                                         yi - offsety, yi + offsety))


        if c is None:
            # defaults to fading "black"
            cdata = 1-data
        else:
            # leave just the alpha to control the fading
            cdata = np.ones(data.shape)

        imarr = np.transpose([cdata*ci[0], cdata*ci[1], cdata*ci[2],
                              data*ci[3]], (1, 2, 0))

        im.set_data(imarr)

        ims.append(im)

    for im in ims:
        ax.add_image(im)

    #ax.autoscale_view()
    # for some reason autoscaling fails for images.  So we'll just force it via
    # scatter...
    sc = plt.scatter(x, y)
    sc.remove()

    return ims
