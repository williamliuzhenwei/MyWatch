Name: Zhenwei Liu Email: zhl012@ucsd.edu PID: A16169244 

Challenge 1: First we plot the error plot by plotting the difference of hr and hr_est, then we choose to do precision and correlation analysis and then plot the result.

Challenge 2: We updated the HRMonitor.py in the library by changing it to the class and added serveral functions to it. When we call HRMonitor.train and HRMonitor.predict, it will train the data set from the data folder and then collect new samples and predict the heart rate with trained gaussian model.

Challenge 3: Finally we get to the complete wearable. First we wrote a function that import datetime and obtain the real time, then we get weather from pyown. We wrote these two together and seperate by comma and return the values. Then we modified the collectsamples function so that it could collect samples for both pedometer and photodetector and return back to the. Lastly, in the main function, we gather the time, weather, steps and heartrate togehter and send it to the MCU to print it on the OLED which eventually print the time on the first line, temperature on the second line, steps on the third line and heart rate on the last line. Also, the MCU will send message "BUZZ" when the steps = 0 to notify the wearer to walk around if they didn't move.
