const int BUTTON_PIN = 14;
unsigned long counter;
int PBUTTON_STATE=HIGH;
int BUTTON_STATE;
int CLOCK_pSTATE=0; //Initialize clock previous state
int CLOCK_STATE=0; //Initialize clock current state
int LOOP_STATE=0;
int TIME_PAST= 0;
int TIMER_100 = millis();
int TIMER_2 = 0;
int TIMER_3 = 0;
int TIMER_0 = 0;
int TIME_OUT;
int TIMER_START = 0;
int TIMER_STOP = 0;
int TIME_PAST_1= 0;
int timer = 0;


void setup() {
 pinMode(BUTTON_PIN, INPUT);
 Serial.begin(9600);
 TIMER_0 = millis();
}

void loop() {

  while(LOOP_STATE == 0){

  if((millis() - TIMER_0) >= 100){  // Print message every 100ms
    Serial.println(timer);
    TIMER_0 = millis();
  }
  
  TIME_OUT = millis() - TIME_PAST;

  BUTTON_STATE = digitalRead(BUTTON_PIN);
  
// If button released, loop state unchange
  if (PBUTTON_STATE == LOW &&  BUTTON_STATE== HIGH && LOOP_STATE == 0 ){
    PBUTTON_STATE = HIGH;
  }
  
// LOOP START
  if (PBUTTON_STATE == HIGH &&  BUTTON_STATE== LOW && LOOP_STATE == 0 ){
    PBUTTON_STATE = LOW;
    timer ++; // Everytime press the button, timer + 1
    TIMER_2 = millis();
  }

  if(millis() - TIMER_2 >= 3000){
    LOOP_STATE = 1;
    TIMER_START = millis();
    TIMER_100 = millis();
  }
}

  while(LOOP_STATE == 1){
// Start counting time
  if((millis() - TIMER_100) >= 100){  // Print message every 100ms
    Serial.println(timer);
    TIMER_2 = millis() - TIME_OUT - TIMER_3;
    
    if(TIMER_2 >= 1000){  // Decrease 1 every 1000ms
        timer = timer - 1;
        TIMER_3 = TIMER_3 + 1000;
      }
    
    TIMER_100 = millis();
  }

  if(timer == 0){ // Time is up, timer stop
    LOOP_STATE = 0;
    TIMER_STOP = millis();
  }

   BUTTON_STATE = digitalRead(BUTTON_PIN);
   
// If button released, loop state unchange.
  if (PBUTTON_STATE == LOW &&  BUTTON_STATE== HIGH && LOOP_STATE == 1 ){
    PBUTTON_STATE = HIGH;
  }

// LOOP STOP
  if (PBUTTON_STATE == HIGH && BUTTON_STATE == LOW && LOOP_STATE == 1){
    PBUTTON_STATE = LOW;
    LOOP_STATE = 0;
    timer ++;
    TIMER_3 = TIMER_3 + 1000;
    TIMER_2 = millis();
    TIMER_STOP = millis();
    TIME_PAST_1 = TIMER_STOP - TIMER_START; //Record the time between one start and stop
    TIME_PAST = TIME_PAST + TIME_PAST_1; //Record the total time between all start and stop
  }
  
  }
}
