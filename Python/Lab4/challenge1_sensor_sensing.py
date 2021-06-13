from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

if __name__ == "__main__":
  num_samples = 100           # 2 seconds of data @ 50Hz
  num_samples_five = 250
  refresh_time = 1            
  
  # add different variables to the circularlist for live plotting
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  
  # 5 seconds ax ay az
  times_five = CircularList([], num_samples_five)
  ax_five = CircularList([], num_samples_five)
  ay_five = CircularList([], num_samples_five)
  az_five = CircularList([], num_samples_five)
  
  ave_x = CircularList([], num_samples_five)
  ave_y = CircularList([], num_samples_five)
  ave_z = CircularList([], num_samples_five)
  
  # 2 seconds sample difference
  ax_diff = CircularList([], num_samples)
  ay_diff = CircularList([], num_samples)
  az_diff = CircularList([], num_samples)
  
  # L-2 norm
  L2_norm = CircularList([], num_samples)
  
  # L-1 norm
  L1_norm = CircularList([], num_samples)
  
  # xyz variance
  ax_vari = CircularList([], num_samples)
  ay_vari = CircularList([], num_samples)
  az_vari = CircularList([], num_samples)
  
  comms = Communication("COM4", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

                


        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        # a. store 5 seconds of data

        times_five.add(int(m1))
        ax_five.add(int(m2))
        ay_five.add(int(m3))
        az_five.add(int(m4))
        # take the average of 250 samples
        ax_avg = np.sum(np.array(ax_five)) / 250
        ay_avg = np.sum(np.array(ay_five)) / 250
        az_avg = np.sum(np.array(az_five)) / 250
        # add the average values to the circularlist
        ave_x.add(int(ax_avg))
        ave_y.add(int(ay_avg))
        ave_z.add(int(az_avg))
        # avg = np.array([ax_avg, ay_avg, az_avg])

       
 

        # b. sample difference of each axis
        # x-axis difference
        ax_3 = np.array([0, 0, 0])
        # take the last 3 data from the ax
        ax_3[0] = np.array(ax[-3])
        ax_3[1] = np.array(ax[-2])
        ax_3[2] = np.array(ax[-1])
        # Compute the difference of adjacent points and take the average
        ax_ave_diff = np.array(((ax_3[2] - ax_3[1]) + (ax_3[1] - ax_3[0])) / 2)
        ax_diff.add(int(ax_ave_diff))

        # y-axis difference
        ay_3 = np.array([0, 0, 0])
        # take the last 3 data from the ay
        ay_3[0] = ay[-3]
        ay_3[1] = ay[-2]
        ay_3[2] = ay[-1]
        # Compute the difference of adjacent points and take the average
        ay_ave_diff = np.array(((ay_3[2] - ay_3[1]) + (ay_3[1] - ay_3[0])) / 2)
        ay_diff.add(int(ay_ave_diff))
        
        # z-axis difference
        az_3 = np.array([0, 0, 0])
        # take the last 3 data from the az
        az_3[0] = az[-3]
        az_3[1] = az[-2]
        az_3[2] = az[-1]
        # Compute the difference of adjacent points and take the average
        az_ave_diff = np.array(((az_3[2] - az_3[1]) + (az_3[1] - az_3[0])) / 2)
        az_diff.add(int(az_ave_diff))
        #print(az_diff)
        
        # c. L-2 norm
        L_2 = np.sqrt(np.power(ax[-1], 2) + np.power(ay[-1], 2)
        + np.power(az[-1], 2))
        L2_norm.add(int(L_2))
        #print(L_2)
        
        # d. L-1 norm
        L_1 = np.sqrt(np.power(ax[-1], 2)) + np.sqrt(np.power(ay[-1], 2)) 
        + np.sqrt(np.power(ax[-1], 2))
        L1_norm.add(int(L_1))
        #print(L_1)
        
        # e. The variance of each axis's data in the last 2 seconds
        ax_var = np.var(ax)
        ay_var = np.var(ay)
        az_var = np.var(az)
        # add the variance values to the circularlist
        ax_vari.add(int(ax_var))
        ay_vari.add(int(ay_var))
        az_vari.add(int(az_var))
        #print(ax_var)
        
        
        # if enough time has elapsed, clear the axis, and plot ax ay az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          plt.cla()
          # plot the original data ax ay az at the top
          plt.subplot(211)
          plt.plot(ax)
          plt.plot(ay)
          plt.plot(az)
          # plot the conversions at the bottom
          plt.subplot(212)
          plt.plot(ax_vari)
          plt.plot(ay_vari)
          plt.plot(az_vari)
          plt.show(block=False)
          plt.pause(0.001)
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
