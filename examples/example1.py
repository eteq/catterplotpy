import numpy as np

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

import catterplot

x = np.linspace(0, 4*np.pi, 25)
y1 = np.sin(x)

plt.plot(x, y1)
catterplot.catter(x, y1, cat=0)

y2 = x/4 + 1
catnums2 = np.arange(len(x)) % catterplot.n_cats()

catterplot.catter(x, y2, c=x, cmap='viridis', cat=catnums2, aspects=1)

plt.savefig('example1.png')
