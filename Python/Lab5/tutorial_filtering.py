import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def l1_norm(ax, ay, az):
  return abs(ax) + abs(ay) + abs(az)

# Load the data as a 500x4 ndarray
data = load_data("./data/8steps_10s_50hz.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]
l1 = l1_norm(ax, ay, az)

plt.subplot(411)
plt.plot(ax)
plt.subplot(412)
plt.plot(ay)
plt.subplot(413)
plt.plot(az)
plt.subplot(414)
plt.plot(l1)
plt.show()