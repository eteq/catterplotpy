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

from __future__ import print_function

import os
import re
import sys

import numpy as np

print ('Execturing catwrite.R script... R must be installed...')
retcode = os.system("R --no-save < catwrite.R")
if retcode != 0:
    print('catwrite.R failed to execute.  Perhaps you need to install R?')
    sys.exit(retcode)


cats = {}
for fn in os.listdir():
    match = re.match(r'cat(\d?\d)', fn)
    if match:
        print("Processing file", fn)
        grpi = int(match.group(1))

        with open(fn) as f:
            rows = [r.strip().split('"')[-1] for r in list(f)[1:]]
            arr =  np.array([[float(e) for e in row.split()] for row in rows])
            assert arr.dtype != 'O'
            cats[grpi] = arr
        print('Removing', fn)
        os.remove(fn)

# most of the cats should be the same shape, and begin at 216 (except for Nyan cat)
catstack = []
for num, cat in cats.items():
    if cat.shape == (72, 288):
        catstack.append(cat[:, 216:])

assert len(catstack) == len(cats)-1
catstack = np.array(catstack)
print('Saving cat stack as cats.npy')
np.save('cats', catstack)
