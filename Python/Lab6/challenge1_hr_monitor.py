# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 22:26:51 2020

@author: 10422
"""
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import sleep
import numpy as np

# Save data to file
def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Collect num_samples from the MCU
def collect_samples():
  num_samples = 500 # 10 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ppg = CircularList([], num_samples)

  comms = Communication("COM4", 115200)
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user and then count down


    input("Ready to collect data? Press [ENTER] to begin.\n")
    print("Start measuring in...")
    for k in range(3,0,-1):
      print(k)
      sleep(1)
    print("Begin!")


    comms.send_message("wearable") # begin sending data

    sample = 0
    while(sample < num_samples):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, _, _, _, m2) = message.split(',')
        except ValueError: # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ppg.add(int(m2))
        sample += 1
        print("Collected {:d} samples".format(sample))

    # a single ndarray for all samples for easy file I/O
    data = np.column_stack([times, ppg])

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    comms.send_message("sleep") # stop sending data
    comms.close()

  return data

# Estimate the sampling rate from the time vector
def estimate_sampling_rate(times):
  return 1 / np.mean(np.diff(times))

if __name__ == "__main__":

  filename = "./data/ppg.csv"
  collect_new_data = True

  # Get data from the MCU and save it if getting new data
  if(collect_new_data):
    data = collect_samples()
    save_data(filename, data)

  # Load the data from file
  data = np.genfromtxt("./data/ppg.csv", delimiter=",")
  t = data[:,0]
  t = (t - t[0])/1e3
  ppg = data[:,1]

# Test the Heart Rate Monitor with offline data
  hr = HRMonitor(500, 50)
  hr.add(t, ppg)
  hr, peaks, filtered = hr.process()

# Plot the results
  plt.plot(t, filtered)
  plt.title("Estimated Heart Rate: {:.2f} bpm".format(hr))
  plt.plot(t[peaks], filtered[peaks], 'rx')
<<<<<<< HEAD
  plt.plot(t, [0.6]*len(filtered), "b--")
=======
  plt.plot(t, [0.55]*len(filtered), "b--")
>>>>>>> 9c938f7254c45109bcd4a5abca6d677e3d1c63e8
  plt.show()
