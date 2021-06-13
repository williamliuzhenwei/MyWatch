int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
//    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
//    writeDisplay("Wearable", 0, true);
  }
  else{
<<<<<<< HEAD
    writeDisplayCSV(command.c_str(), 2);
=======
    writeDisplayCSV(command.c_str(), 0);
>>>>>>> 9c938f7254c45109bcd4a5abca6d677e3d1c63e8
  }

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
  }
}
