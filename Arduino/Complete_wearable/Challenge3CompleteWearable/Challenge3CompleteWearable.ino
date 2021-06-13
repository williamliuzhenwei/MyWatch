int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0;         
int ay = 0;
int az = 0;
bool sending = false;
int ppg = 0;
int buzz_state=0;
unsigned long buzz_time;
//Button
const int BUTTON_PIN =14; 
// LED
const int LED_PIN = 13;

void setup() {
  // put your setup code here, to run once:
  setupCommunication();
  setupDisplay();
  setupAccelSensor();
  setupMotor();
  setupPhotoSensor();
  sending = false;
  pinMode(BUTTON_PIN,INPUT);
  pinMode(LED_PIN,OUTPUT);
}

void loop() {
// If the button is pressed down, the led will light up. (If it's a high power LED, it can act as a torch
 if(digitalRead(BUTTON_PIN)==LOW){
  digitalWrite(LED_PIN,HIGH);
 }
  else{
  digitalWrite(LED_PIN,LOW);
 }
 

  String command = receiveMessage();
  if(command == "sleep"){
    sending = false;
  }
  else if(command == "wearable"){
    sending = true;
  }

  // if the steps = 0, the motor will buzz for 2 seconds, to notice the wearer.
  else if(command == "BUZZ"){
    activateMotor(255);
    buzz_time = millis();
  }
  
    
  // seperate the things we don't wanna print on the LED
  else if(command != "BUZZ" && command != "wearable" && command != "sleep" && command != "wear" && command != "able" && command != "slee"){
    // seperate the messgae by comma.
    writeDisplayCSV(command.c_str(), 3);
  }

  // if the steps = 0, the motor will buzz for 2 seconds.
  if(millis() - buzz_time >= 2000){
      deactivateMotor();
    }
 
  //send both ax ay az and ppg data   
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az) + "," + String(ppg) ;
    sendMessage(response);  
  }
  
}
