Name: Zhenwei Liu Email: zhl012@ucsd.edu PID: A16169244
Challenge 1 is to read 500 samples and after filtering it, count the total amount of peaks. There are several steps of filtering such as
compute the L1 norm, moving average, gradient, spectral density and Low pass filter design. Under a 50 Hz communication rate,
500 samples would be 10 seconds of data and spyder will print out the plot with filtered graph and the threshhold lines. 


Challenge 2 is basically the real time version of challenge 1. In my code, I chose to collect 250 samples which is 5 seconds
of data. Then spyder will filter these 250 samples and makes it smooth so that we won't count shifted peaks multiple times.
After that, I used a while(1) so this process will keep going and I set another variable to store the count of peaks and print it to the OLED.
Ideally, the MCU would show the counted steps up every 5 seconds. 
