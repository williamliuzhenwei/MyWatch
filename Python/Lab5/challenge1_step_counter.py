from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from ECE16Lib.Pedometer import Pedometer
from time import sleep
import numpy as np


def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def l1_norm(ax, ay, az):
  return abs(ax) + abs(ay) + abs(az)

def collect_samples():

  num_samples = 500 # 10 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  comms = Communication("COM4", 115200)
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user to start walking before starting to collect data
    input("Ready to collect data? Press [ENTER] to begin.\n")
    sleep(3)
    comms.send_message("wearable") # begin sending data

    sample = 0
    while(sample < num_samples):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError: # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        sample += 1
        print("Collected {:d} samples".format(sample))

    # a single ndarray for all samples for easy file I/O
    data = np.column_stack([times, ax, ay, az])

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    comms.send_message("sleep") # stop sending data
    comms.close()

  return data

if __name__ == "__main__":


  # Make sure not to overwrite a file after saving!
  filename = "./data/accelerometer.csv"

  # Get data from the MCU and save to file
  data = collect_samples()
  save_data(filename, data)

  # Load the data from file
  data = load_data(filename)


  # Data is 500x4 containing the time, ax, ay, az samples
  t = data[:,0]

  t = (t - t[0])/1e3 # make time range from 0-10 in seconds
  ax = data[:,1]
  ay = data[:,2]
  az = data[:,3]
  t_high = 500   # remember to keep the same as Pedometer setting
  t_low = 25
  
  ped = Pedometer(500, 50, [])
  ped.add(ax, ay, az)
  steps, peaks, filtered = ped.process()
  # Compute the Sample L1 Norm 


  # Plot the data
  plt.plot(t, filtered)
  plt.title("Detected Peaks = %d" % steps)
  plt.plot(t[peaks], filtered[peaks], 'rx')
  plt.plot(t, [t_high]*len(filtered), "b--")
  plt.plot(t, [t_low]*len(filtered), "b--")
  plt.show()



    