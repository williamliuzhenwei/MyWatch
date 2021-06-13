const int BUTTON_PIN = 14;
int PBUTTON_STATE = HIGH;
int BUTTON_STATE;
int LOOP_STATE=0;
int TIMER_1 = 0;
int TIMER_2 = 0;
int TIMER_3 = 0;
int TIMER_4 = 0;
int TIME_OUT;
int TIMER_START = 0;
int TIMER_STOP = 0;
int TIME_PAST= 0;
int TIME_PAST_1= 0;
int sampleTime = 0; 
int ax = 0, ay = 0, az = 0;
int numTaps = 0;
int reset_time = 0;

//detect when the accelerometer is tapped
int detectTaps(){
  sampleSensors();
  if(ax >= 1890 || ax<= 1800 || ay >= 1890 || ay <= 1800 || az >= 2390 || az <= 2320){
    delay(100);
    return 1;
  }
  return 0;
}

//When button is pressed for 2 seconds, numTaps reset to 0
void detectReset() {
  BUTTON_STATE = digitalRead(BUTTON_PIN);
  if (PBUTTON_STATE == HIGH && BUTTON_STATE == LOW){
    reset_time = millis();
  }
  PBUTTON_STATE = BUTTON_STATE;
  BUTTON_STATE = digitalRead(BUTTON_PIN);
  if (PBUTTON_STATE == LOW && BUTTON_STATE == LOW){
    if((millis() - reset_time) >= 2000){
      reset_time = millis();
      numTaps = 0;
      String message = String(numTaps);
      writeDisplay(message.c_str(), 2, true);
    }
  }
}

void TotalTimePast() {
    TIMER_2 = millis();
    TIMER_STOP = millis();
    TIME_PAST_1 = TIMER_STOP - TIMER_START; //Record the time between one start and stop
    TIME_PAST = TIME_PAST + TIME_PAST_1; //Record the total time between all start and stop
}

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  setupAccelSensor();
  setupDisplay();
  String message = String(numTaps);
  writeDisplay(message.c_str(), 2, true);
  setupMotor();
  deactivateMotor();
}
  
void loop() {
while(LOOP_STATE == 0){
  detectReset();

  //When numtaps = 0, motor buzz
  if(numTaps == 0){
    activateMotor(255);
  }
  if(numTaps != 0){
    deactivateMotor();
  }

    String message = String(numTaps);
    writeDisplay(message.c_str(), 2, true);

//detect tap
  if (detectTaps() == 1){
    numTaps++;
    TIMER_4 = millis();
  }

  // delay 4s to enter counting down state
  if(millis() - TIMER_4 >= 4000){  
    TIMER_START = millis();
    TIME_OUT = millis() - TIME_PAST;
    LOOP_STATE = 1;
  }
}

//counting down state
while(LOOP_STATE == 1){
  detectReset();
    
    TIMER_2 = millis() - TIME_OUT - TIMER_3;
    if(TIMER_2 >= 1000){  // Decrease 1 every 1000ms
        numTaps = numTaps - 1;
        TIMER_3 = TIMER_3 + 1000;
        Serial.println(numTaps);
        String message = String(numTaps);
        writeDisplay(message.c_str(), 2, true);
      }
   
    if (detectTaps() == 1){  //detect tap, count down stop
    numTaps ++;
    TotalTimePast();
    TIMER_4 = millis();
    LOOP_STATE = 0;
   }

  if (numTaps == 0){ // numTaps = 0, LOOP STOP
    TotalTimePast();
    LOOP_STATE = 0;
  }
}



}
