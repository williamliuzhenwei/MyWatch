from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from time import time
import numpy as np

if __name__ == "__main__":
  num_samples = 100     
  
  
  # add two seconds of samples to the circular list 
  ay_two = CircularList([], num_samples)
  
  # add the average of two seconds of samples to the circular list 
  ave_y = CircularList([], num_samples)
  
  # add the difference of the averages to the circular list
  ay_diff = CircularList([], num_samples)


  
  comms = Communication("COM4", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    # initialize the timing
    timer_2 = time()
    timer = time()
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:       
          continue
          
        # I collect 100 samples and average them,
        # Then compare the difference of samples of the last 5 averages.
        ay_two.add(int(m3))
        ay_avg = np.sum(np.array(ay_two)) / 100
        # add average value to the circularlist
        ave_y.add(int(ay_avg))
        ay_3 = np.array([0, 0, 0, 0, 0])
        # extract the last 5 average values from ave_y
        ay_3[0] = ave_y[-5]
        ay_3[1] = ave_y[-4]
        ay_3[2] = ave_y[-3]
        ay_3[3] = ave_y[-2]
        ay_3[4] = ave_y[-1]
        ay_ave_diff = np.array(((ay_3[4] - ay_3[3]) 
                                + (ay_3[3] - ay_3[2]) 
                                + (ay_3[2] - ay_3[1]) 
                                + (ay_3[1] - ay_3[0])) / 4)
        ay_diff.add(int(ay_ave_diff))
        
        # Took the absolute value of the difference
        sensor = np.sqrt(np.power(ay_ave_diff,2))
        
        
      #  check if the data is reasonable
        print(sensor)
        
        # if the sensor moves too big, reset the timer_2
        if sensor > 0.25:
             timer_2 = time()
        
        # if the MCU has been inactive for 5 seconds, go to IDLE
        if (time() - timer_2) >= 5:
             comms.send_message("IDLE") # MCU will read IDLE and go to state IDLE
             timer_2 = time() 
        
        # if the sensor didn't move, reset timer
        if sensor <= 0.25:
             timer = time()
         
        # if the MCU has been active for 1 seconds, go the ACTIVE
        if ((time() - timer) >= 1):
             comms.send_message("ACTIVE") # MCU will read ACTIVE and go to state ACTIVE

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
