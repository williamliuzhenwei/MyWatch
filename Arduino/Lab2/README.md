Lab2, Zhenwei Liu, Date: 10/19/2020
This lab asks us to build a gesture control unit. There are different states in this control unit. When you tab the accelerometer, the control unit will add one to numTaps, and if no accelerometer reads in 4 second, the timer kicks in and countdown time. Anytime the accelerometer reads an input will stop the timer and add one to numTaps. Also, when button is pressed for 2 seconds, numTaps will reset to 0. Lastly, when timer counts down to 0, the motor will buzz. I built multiple functions to fulfill different requirements.