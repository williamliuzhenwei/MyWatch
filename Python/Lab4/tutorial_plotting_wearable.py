from ECE16Lib.Communication import Communication
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
  num_samples = 500               # 10 seconds of data @ 50Hz
  times = np.zeros((num_samples)) # vectors, not matrices
  ax = np.zeros((num_samples))
  ay = np.zeros((num_samples))
  az = np.zeros((num_samples))

  comms = Communication("COM4", 115200)
  print(comms)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    count = 0
    while(count < num_samples):
      message = comms.receive_message()
      if(message != None):
        (m1, m2, m3, m4) = message.split(',')
        times[count] = int(m1)
        ax[count] = int(m2)
        ay[count] = int(m3)
        az[count] = int(m4)
        count += 1
        print("Sample:",count, "t:",m1, "ax:",m2, "ay:",m3, "az:",m4)
    comms.send_message("sleep")   # stop sending data
    comms.close()

  except(Exception, KeyboardInterrupt) as e:
    print(e)                      # Exiting the program due to exception
    comms.send_message("sleep")   # stop sending data
    comms.close()
    exit()

# Switch time axis to start from 0, convert from ms to seconds, and plot!
  times = (times - times[0]) / 1e3
  plt.subplot(311)
  plt.plot(times, ax)
  plt.subplot(312)
  plt.plot(times, ay)
  plt.subplot(313)
  plt.plot(times, az)
  plt.show()

#/dev/cu.ECE16-ESP32_SPP_SERVER
#/dev/cu.usbserial-14120