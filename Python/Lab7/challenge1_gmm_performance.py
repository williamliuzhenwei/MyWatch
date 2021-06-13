#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 22:14:33 2020

@author: siyuanzhang
"""

# Import for searching a directory
import glob

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
import math
# The GMM Import
from sklearn.mixture import GaussianMixture as GMM

# Import for Gaussian PDF
from scipy.stats import norm

# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "/*")
  return [filepath.split("/")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
  filepath = glob.glob(search_key)[0]
  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)
  if(fs_est < fs-1 or fs_est > fs):
    print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

  return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

# Save data to file
def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  fs = 50
  directory = "./data"
  subjects = get_subjects(directory)
 # Leave-One-Subject-Out-Validation
  # 1) Exclude subject
  # 2) Load all other data, process, concatenate
  # 3) Train the GMM
  # 4) Compute the histogram and compare with GMM
  # 5) Test the GMM on excluded subject
  for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # Compare the histogram with the GMM to make sure it is a good fit

    plt.hist(train_data, 100, density=True)
    plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
    plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
    plt.show()


    # Test the GMM on excluded subject
    print("Testing - all trials of subject: %s" % exclude)
    error = []
    precision = []
    correlation = []
    HR =[]
    HR_EST=[]
    correlation = []
    for trial in range(1,11):
      x = 0
      t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
      test_data = process(ppg)

      labels = gmm.predict(test_data.reshape(-1,1))

      hr_est, peaks = estimate_hr(labels, len(ppg), fs)
      print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))
      #plt.scatter(hr,hr_est)
      
      
      RMSE = math.sqrt( ((hr_est - hr)**2)/trial)
      er = abs(hr - hr_est)
      error.append(er)
     #precision
      pre = abs((hr_est - hr)) / hr_est * 100
      precision.append(pre)
     # correlation
      HR.append(hr)
      HR_EST.append(hr_est)
      
     
     
      #plt.plot(t, test_data)
      #plt.plot(t, peaks)
      #plt.show()
    # calculate corr
    HR_AVG = sum(HR)/10
    HR_EST_AVG = sum(HR_EST) / 10
    
    for i in range(0,10):
        corr = ((HR[i]- HR_AVG)*(HR_EST[i] - HR_EST_AVG)) / (math.sqrt(((HR[i]- HR_AVG)**2)*((HR_EST[i] - HR_EST_AVG)**2)))
        correlation.append(corr)
    
    
    t = [1,2,3,4,5,6,7,8,9,10]
    plt.xlabel("Trials")
    plt.scatter(t,error)
    plt.ylabel("ERROR")
    #plt.scatter(t,precision)
    #plt.ylabel("precision error(%)")
    #plt.scatter(t,correlation)
    #plt.ylabel("Correlation")
    plt.show()
    
    
    
    
    
    
    
    
    
    
