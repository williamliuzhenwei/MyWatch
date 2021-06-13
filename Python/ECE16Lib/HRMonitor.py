#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:31:54 2020

@author: siyuanzhang
"""

from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
import glob

import matplotlib.pyplot as plt

from ECE16Lib.Communication import Communication
# The GMM Import


# Import for Gaussian PDF
from scipy.stats import norm
"""
A class to enable a simple heart rate monitor
"""
class HRMonitor:
  """
  Encapsulated class attributes (with default values)
  """
  __hr = 0           # the current heart rate
  __time = None      # CircularList containing the time vector
  __ppg = None       # CircularList containing the raw signal
  __filtered = None  # CircularList containing filtered signal
  __num_samples = 0  # The length of data maintained
  __new_samples = 0  # How many new samples exist to process
  __fs = 0           # Sampling rate in Hz
  __thresh = 0.6     # Threshold from Tutorial 2
  __directory = None 
  """
  Initialize the class instance
  """
  def __init__(self, num_samples=0, fs=0, times=[], data=[]):
    self.__hr = 0
    self.__num_samples = num_samples
    self.__fs = fs
    self.__time = CircularList(data, num_samples)
    self.__ppg = CircularList(data, num_samples)
    self.__filtered = CircularList([], num_samples)
    self.__directory = "./data"
    self.__filename = "./data/ppg.csv"
    
  """
  Add new samples to the data buffer
  Handles both integers and vectors!
  """
  def add(self, t, x):
    if isinstance(t, np.ndarray):
      t = t.tolist()
    if isinstance(x, np.ndarray):
      x = x.tolist()


    if isinstance(x, int):
      self.__new_samples += 1
    else:
      self.__new_samples += len(x)

    self.__time.add(t)
    self.__ppg.add(x)

  """
  Compute the average heart rate over the peaks
  """
  def compute_heart_rate(self, peaks):
    t = np.array(self.__time)
    return 60 / np.mean(np.diff(t[peaks]))

  """
Process the new data to update step count
  """
  def process(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__ppg[ -self.__new_samples: ])

    # Filter the signal (feel free to customize!)
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    x = filt.normalize(x)

    # Store the filtered data
    self.__filtered.add(x.tolist())

    # Find the peaks in the filtered data
    _, peaks = filt.count_peaks(x, self.__thresh, 1)

    # Update the step count and reset the new sample count
    self.__hr = self.compute_heart_rate(peaks)
    self.__new_samples = 0

    # Return the heart rate, peak locations, and filtered data
    return self.__hr, peaks, np.array(self.__filtered)

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__steps = 0
    self.__time.clear()
    self.__ppg.clear()
    self.__filtered = np.zeros(self.__num_samples)

  # Retrieve a list of the names of the subjects
  def get_subjects(self,directory):
    filepaths = glob.glob(directory + "/*")
    return [filepath.split("/")[-1] for filepath in filepaths]
  
# Retrieve a data file, verifying its FS is reasonable
  def get_data(self,directory, subject, trial, fs):
    search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
    t = (t-t[0])/1e3
    hr = self.get_hr(filepath, len(ppg), fs)

    fs_est = self.estimate_fs(t)
    if(fs_est < fs-1 or fs_est > fs):
        print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

    return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
  def get_hr(self,filepath, num_samples, fs):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = num_samples / fs
    return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
  def estimate_fs(self,times):
    return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
  def process1(self,x):
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
  def plot_gaussian(self,weight, mu, var):
    weight = float(weight)
    mu = float(mu)
    var = float(var)

    x = np.linspace(0, 1)
    y = weight * norm.pdf(x, mu, np.sqrt(var))
    plt.plot(x, y)

# Estimate the heart rate given GMM output labels
  def estimate_hr(self,labels, num_samples, fs):
    peaks = np.diff(labels, prepend=0) == 1
    count = sum(peaks)
    seconds = num_samples / fs
    hr = count / seconds * 60 # 60s in a minute
    return hr, peaks

# Save data to file
  def save_data(self,filename, data):
    np.savetxt(filename, data, delimiter=",")

# Load data from file
  def load_data(self,filename):
    return np.genfromtxt(filename, delimiter=",")


  def train(self):
   fs = 50
   directory = "./data"
   subjects = self.get_subjects(directory)
   for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = self.get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, self.process1(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)
    
    print("Testing - all trials of subject: %s" % exclude)
   
    for trial in range(1,11):
     
      t, ppg, hr, fs_est = self.get_data(directory, exclude, trial, fs)
      test_data = self.process1(ppg)

      labels = gmm.predict(test_data.reshape(-1,1))

      hr_est, peaks = self.estimate_hr(labels, len(ppg), fs)
      print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))


#get samples

# Collect num_samples from the MCU
  def collect_samples(self):
       num_samples = 250 # 10 seconds of data @ 50Hz
       times = CircularList([], num_samples)
       ppg = CircularList([], num_samples)
       comms = Communication("/dev/cu.ECE16-ESP32SPP", 115200)
       try:
           comms.clear() # just in case any junk is in the pipes
    # wait for user and then count down

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
       
  def estimate_sampling_rate(self,times):
        return 1 / np.mean(np.diff(times))

  def predict(self):
      filename = "./data2/ssss/ppg.csv"
      while(1):
  # Load the data from file
           data = self.collect_samples()
           self.save_data(filename, data)
  
           data = np.genfromtxt(filename, delimiter=",")
           t = data[:,0]
           t = (t - t[0])/1e3
           ppg = data[:,1]
           hr = HRMonitor(250, 50)
           hr.add(t, ppg)
           hr, peaks, filtered = hr.process()
  
           fs = 50
           train_data = np.array([])
           train_data = np.append(train_data, self.process1(ppg))
           train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
           gmm = GMM(n_components=2).fit(train_data)
           test_data = self.process1(ppg)

           labels = gmm.predict(test_data.reshape(-1,1))

           hr_est, peaks = self.estimate_hr(labels, len(ppg), fs)
           print(" HR: %3.2f, HR_EST: %3.2f" % (hr,hr_est))
          
          
# Plot the results
           plt.plot(t, filtered)
           plt.title("Estimated Heart Rate: {:.2f} bpm".format(hr))
           plt.plot(t[peaks], filtered[peaks], 'rx')
           plt.plot(t, [0.55]*len(filtered), "b--")
           plt.show()