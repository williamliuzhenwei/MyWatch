Name: Zhenwei Liu Email: zhl012@ucsd.edu PID: A16169244

Challenge 1: This challenge is basically asking us to plot different conversions of the original data
and then compare them with the original ax ay az. Also it asks us to live plot those conversions, so
after we compute the conversions, we need to make them numpy array and add them to the circularlist

Challenge 2: This challenge is asking us to detect the idle state and active state. For my code, I used 
the sample difference of the axis to determine if the accelerometer is moved or not. If the sample difference
is small enough, after 5 seconds it will send a message "IDLE" to the MCU, and MCU will print that and buzz the 
motor for 1 second. Similar to the active state, after 1 second of moving the accelerometer, it will send a 
message "active" to the MCU, and MCU will print "You are active!" untill it goes back to IDLE state.

Challenge 3: I build a class called My_watch and two methods under it. The first method is called stream.
When I call this method, it will show the live plot of the accelerometer with ax ay and az on the same graph.
The second method is called detect. If this method is called, it will detect two states "IDLE" and "ACTIVE".
If the accelerometer is not moved in 5 seconds, it will send a message "IDLE" to MCU, and OLED will print
"Time to walk!" If the accelerometer is moved for 1 second, it will send a message "ACTIVE" to MCU, and OLED 
will print "Great job!". I used ECE16 = My_watch("ECE16") to instantiate it. And call different method seperately.
