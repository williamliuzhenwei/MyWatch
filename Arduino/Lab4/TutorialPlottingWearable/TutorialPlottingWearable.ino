int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0;         
int ay = 0;
int az = 0;
int timer_1;
bool sending = false;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupMotor();
  deactivateMotor();
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep"){
    sending = false;
  }
  else if(command == "wearable"){
    sending = true;
  }

  if(command == "IDLE"){
    writeDisplay("Time to walk!", 0, true);
    activateMotor(255);
    timer_1 = millis();
  }
  
  if ((millis() - timer_1) >= 1000){
    deactivateMotor();
  }
  
  if (command == "ACTIVE"){
    writeDisplay("Great job!", 0 ,true);
    deactivateMotor();
  }
    
    
  
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}
