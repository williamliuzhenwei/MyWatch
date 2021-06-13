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
int TIME_OUT;
int TIMER_START = 0;
int TIMER_STOP = 0;
int TIME_PAST_1= 0;


void setup() {
 pinMode(BUTTON_PIN, INPUT);
 Serial.begin(9600);
}

void loop() {

  while(LOOP_STATE == 0){ // Timer stop

  TIME_OUT = millis() - TIME_PAST; // The amount of time that the timer is off
  
  BUTTON_STATE = digitalRead(BUTTON_PIN);
  
// If button released, loop state unchanged
  if (PBUTTON_STATE == LOW &&  BUTTON_STATE== HIGH && CLOCK_pSTATE == 0 ){
    PBUTTON_STATE = HIGH;
  }
  
// LOOP START
  if (PBUTTON_STATE == HIGH &&  BUTTON_STATE== LOW && CLOCK_pSTATE == 0 ){
    LOOP_STATE = 1;
    CLOCK_STATE = 1;
    PBUTTON_STATE = LOW;
    CLOCK_pSTATE = CLOCK_STATE;  
    TIMER_START = millis();
    TIMER_100 = millis(); 
  }

  }

  while(LOOP_STATE == 1){ // Timer start
    
// Start counting time
  if((millis() - TIMER_100) >= 100){  // Print message every 100ms
    Serial.println(counter);
    TIMER_2 = millis() - TIMER_3 - TIME_OUT;
    
    if( TIMER_2 >= 1000){  // Add 1 to counter every 1000ms
        counter ++;
        TIMER_3 = TIMER_3 + 1000;
      }
    
    TIMER_100 = millis();
  }

   BUTTON_STATE = digitalRead(BUTTON_PIN);
   
// If button released, loop state unchanged
  if (PBUTTON_STATE == LOW &&  BUTTON_STATE== HIGH && CLOCK_pSTATE == 1 ){
    PBUTTON_STATE = HIGH;
  }

// LOOP STOP
  if (PBUTTON_STATE == HIGH && BUTTON_STATE == LOW && CLOCK_pSTATE == 1){
    LOOP_STATE = 0;
    CLOCK_STATE = 0; 
    PBUTTON_STATE = LOW;
    CLOCK_pSTATE = CLOCK_STATE;  
    TIMER_STOP = millis();
    TIME_PAST_1 = TIMER_STOP - TIMER_START; //Record the time between one start and stop
    TIME_PAST = TIME_PAST + TIME_PAST_1; //Record the total time between all start and stop
  }
  }
  
}
