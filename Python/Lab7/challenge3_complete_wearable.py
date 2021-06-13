from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
import numpy as np
from ECE16Lib.Pedometer import Pedometer

# get weather
def weather():
    
    from pyowm import OWM
    owm = OWM('53ac843f008f1243459e1f69d918a585').weather_manager()
    weather = owm.weather_at_place('San Diego,CA,US').weather
    curr_weather = str(weather.temperature('fahrenheit')['temp'])
    return curr_weather

# get date
def date():
    from datetime import date
    today_date = date.today()
    str_datetime = today_date.strftime("%m-%d-%y")
    #print("Today's date:", today)
    return str_datetime

# put temp and time together and return
def interval():
   from datetime import datetime
   time_now = datetime.now()
   current_time = time_now.strftime("%H:%M")
   z = "TEMP:" +weather()
   x = "TIME:"+current_time
   out = x+","+ z
   time_now = datetime.now()
   current_time = time_now.strftime("%H:%M:%S")
   return out


# Save date to file
def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def l1_norm(ax, ay, az):
  return abs(ax) + abs(ay) + abs(az)

# process pedometer data
def run_data(data):
    filename = "./data3/accelerometer.csv"
   
    save_data(filename, data)
    data = load_data(filename)
    t = data[:,0]

    t = (t - t[0])/1e3 # make time range from 0-10 in seconds
    ax = data[:,1]
    ay = data[:,2]
    az = data[:,3]
    
    ped = Pedometer(200, 50, [])
    ped.add(ax, ay, az)
    return ped

# collect samples from MCU for both pedometer and hrmonitor
def collect_samples():

  # collect time, ax, ay, az and ppg together
  num_samples = 250 # 5 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  ppg = CircularList([], num_samples)
  
  comms = Communication("/dev/cu.ECE16-ESP32SPP", 115200)
 
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user to start walking before starting to collect data
    
    comms.send_message("wearable") # begin sending data
   
    sample = 0
    
    while(sample < num_samples):
      message = comms.receive_message()
      if(message != None):
        try:
            # Collect both ax ay az and hr
          (m1, m2, m3, m4, m5) = message.split(',')
        except ValueError: # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        ppg.add(int(m5))
        sample += 1
        print("Collected {:d} samples".format(sample))

    # a single ndarray for all samples for easy file I/O
   
    data = np.column_stack([times, ax, ay, az])
    
    # put ppg and times to data2
    data2 = np.column_stack([times, ppg])

    ped = run_data(data)
    
    # save ppg data to the path
    save_data("./data2/ssss/ppg.csv", data2)
    
    steps, peaks, filtered = ped.process()
    return steps
    
    

    
  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    comms.send_message("sleep") # stop sending data
    comms.close()


"""
Main entrypoint for the application
"""
if __name__== "__main__":

    comms = Communication("/dev/cu.ECE16-ESP32SPP", 115200)
    count = 0
    
    # assign HRMonitor returned value to hrm and train
    hrm = HRMonitor() 
   # hrm.train()
   
    while (True):
        
      # get the time and weather
      watch = interval()
      
      # collect the data of steps and hr
      steps = collect_samples()
      
      # accumalte steps 
      count = count + steps
      
      # If MCU didn't move, steps = 0, then the motor will buzz
      if count==0:
          comms.send_message(("BUZZ"))
      hr = hrm.predict()
      
      # If the hr is too high or too low, it will show 0.00 (Not detected)
      if (hr > 150 or hr < 50):
          hr = "0.00"
      
      # combine time, date, steps and hr_est using comma to seperate
      message = watch +","+"steps:"+str(count) +"," +"HR:"+str(hr)
      
      #check the messgae
      print(message)
      
      # send time, date, steps and hr_est to the MCU
      comms.send_message(message)


