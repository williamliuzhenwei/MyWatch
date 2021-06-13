# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 01:09:21 2020

@author: 10422
"""
from pyowm import OWM

#obtain the temperature information
def get_temperature():
    global weather
    owm = OWM('6d1f9a23388bc436ea0d8454790a36a7')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('San Diego, US')
    w = observation.weather
    temperature = w.temperature('fahrenheit')
    return temperature

#get today's date
def get_date():
    global today
    from datetime import date
    today = date.today()
    return today

#get current time
def get_time():
    import time
    global current_time
    from datetime import datetime
    current = datetime.now()
    current_time = current.strftime("%H:%M:%S")
    time.sleep(1)
    return current_time


import serial
 
def setup(serial_name, baud_rate):
     ser = serial.Serial(serial_name, baudrate=baud_rate)
     return ser
 
def close(ser):
     ser.close()
     
def send_message(ser, message):
    if(message[-1] != '\n'):
        message = message + '\n'
    ser.write(message.encode('utf-8'))
    
def receive_message(ser, num_bytes=50):
      if(ser.in_waiting > 0):
          return ser.readline(num_bytes).decode('utf-8')
      else:
          return None
 
    
def main():
    LOOP_STATE = 1
    while LOOP_STATE == 1: # continuously print out 
        temp = str(get_temperature()) #change to string
        today = str(get_date())
        current_time = str(get_time()) 
        ser = setup("COM4", 115200)
        send_message(ser, current_time + "," + today + "," + temp[1:11])
        message = receive_message(ser)
        print(message)
        close(ser)
 
 
if __name__== "__main__":
     main()
