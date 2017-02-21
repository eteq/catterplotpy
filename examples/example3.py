import numpy as np
from scipy import polyfit, polyval

import matplotlib
matplotlib.use('agg')

from matplotlib import pyplot as plt

from catterplot import catter

datastr = """
1020	0
1070	2
1325	11
1515	17
1650	23
1770	29
2084	38
2600	52
2840	68
3635	103
3773	111
4025	131
4081	131
4363	139
4419	140
4846	160
5227.272727	173
"""

days = []
grams = []
for row in datastr.strip().split('\n'):
    gram, day = row.split()
    grams.append(float(gram))
    days.append(float(day))
days = np.array(days)
lbs = 2.2*np.array(grams)/1000

coeffs = polyfit(days, lbs, 1)
xfit = np.linspace(days[0]-25, days[-1]+25, 100)
plt.plot(xfit, polyval(coeffs, xfit), ls='--', c='r')

catter(days, lbs, s=250, aspects='auto')

plt.xlabel('days since adoption')
plt.ylabel('weight [lbs]')
plt.title('The Growth of Kepler Ganymede')

plt.xlim(xfit[0], xfit[-1])
plt.ylim(0, plt.ylim()[-1])

plt.savefig('example3.png')
