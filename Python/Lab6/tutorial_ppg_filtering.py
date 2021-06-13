# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:59:39 2020

@author: 10422
"""

import ECE16Lib.DSP as filt
from matplotlib import pyplot as plt
import numpy as np

# Load the data as a 500x2 ndarray and extract the 2 arrays
data = np.genfromtxt("./data/ramsink_01_13.csv", delimiter=",")
t = data[:,0]
t = (t - t[0])/1e3
ppg = data[:,1]

# Detrend the signal and plot the result
dt = filt.detrend(ppg, 25)

ma = filt.moving_average(dt, 5)
grad = filt.gradient(ma)

norm = filt.normalize(grad)

plt.subplot(211)
plt.title("Normalize")
plt.plot(t, ppg)
plt.subplot(212)
plt.plot(t, norm)
plt.show()