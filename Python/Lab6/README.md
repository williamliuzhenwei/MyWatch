Name: Zhenwei Liu Email: zhl012@ucsd.edu PID: A16169244 
For Tutorial 1:
1) Because the addressing scheme allows the microcontroller to select which device to communicate. So that different devices can share the same port.

2) If the device is not connected, the error messgae will occur. If the error is printed, and then connect the device, the code 
   particalSensor.begin will not proceed.
   
3) Then the photodetector won't be able to measure the volume of the blood going though. 

4) The unit for pulseWidth is micrometer (um). A bigger pulse width will result in a less intense measurement. Because the width between
   the peaks is bigger, so that the period is bigger. Thus the measurement will be less intense.
   
5) 15 bits would be needed for range of 16384

6) Red led peak wavelength is 660, IR led peak wavelength is 880, Green led peak wavelength is 537.

7) Led mode would be 3. photoSensor.getG()

Challenge 1: First I collect data from MCU and call HRMonitor to filter the plot. Then I modified the thresh value from 6.0 to 5.55. 
Because when I collect the data and observe the graph, I found that sometimes some peaks with lower values would be ignored. 
After lower the thresh value, the algorithm is pretty good which could detect most of the peaks without double counting. 

Challenge 2: This challenge is basically the same as Challenge 1. I added a while(1) loop to keep the code proceeding 
and update the heart beats per minutes every 5 seconds. Then I push the number of the BPM to MCU and display 
the number on MCU and refresh every 5 seconds.
