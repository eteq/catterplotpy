import numpy as np

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

import catterplot

np.random.seed(12345)
x, y = np.random.randn(2, 50)
sizes = np.random.rand(len(x))*10+20

catterplot.catter(x, y, s=sizes, cat='random')

plt.xlim(-3, 3)
plt.ylim(-3, 3)

plt.title('Cats are so random!')

plt.savefig('example2.png')
