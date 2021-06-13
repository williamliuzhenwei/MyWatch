    int LED_PIN_BLUE = 12;
    int LED_PIN_YELLOW = 13;
    int LED_PIN_RED = 14;
    unsigned long time0, time1, time2, time3;
    unsigned long LED_BLUE_timer;
    unsigned long LED_YELLOW_timer;
    unsigned long LED_RED_timer;
void setup()
{
    pinMode(LED_PIN_BLUE, OUTPUT);
    pinMode(LED_PIN_YELLOW, OUTPUT);
    pinMode(LED_PIN_RED, OUTPUT);
    time1 = millis();
    time2 = millis();
    time3 = millis();
    
}

void loop()
{
////////////////////////////////////////////////////////////////////////////////
// Challenge 1 Part 1, condition a,b,c
////////////////////////////////////////////////////////////////////////////////
    {
    digitalWrite(LED_PIN_RED, HIGH);
    LED_RED_timer = millis();
    if (LED_RED_timer - time3 < 500)
    {
      digitalWrite(LED_PIN_RED, LOW);
    }
        else if((LED_RED_timer - time3) >= 500 && (LED_RED_timer - time3) < 1000)
        {
        digitalWrite(LED_PIN_RED, HIGH);
        }
          else if ((LED_RED_timer - time3) >= 1000)
          {
          time3 = millis();
          }
    {
    digitalWrite(LED_PIN_BLUE, HIGH);
    LED_BLUE_timer = millis();
    if ((LED_BLUE_timer - time1) < 50)
    {
      digitalWrite(LED_PIN_BLUE, LOW);
    }
      else if ((LED_BLUE_timer - time1) >= 50 && (LED_BLUE_timer - time1) < 100)
      {
        digitalWrite(LED_PIN_BLUE, HIGH);
      }
        else if ((LED_BLUE_timer - time1) >= 100)
        {
          time1 = millis();
        }
    } 
    {
    digitalWrite(LED_PIN_YELLOW, HIGH);
    LED_YELLOW_timer = millis();
    if (LED_YELLOW_timer - time2 < 10)
    {
      digitalWrite(LED_PIN_YELLOW, LOW);
    }
      else if ((LED_YELLOW_timer - time2) >= 10 && (LED_YELLOW_timer - time2) < 20)
      {
        digitalWrite(LED_PIN_YELLOW, HIGH);
      }
        else if ((LED_YELLOW_timer - time2) >= 20)
        {
          time2 = millis();
        }
    }
    }
////////////////////////////////////////////////////////////////////////////////
//  Challenge 1 Part 2, condition a, b, c
////////////////////////////////////////////////////////////////////////////////
    {
    digitalWrite(LED_PIN_RED, HIGH);
    LED_RED_timer = millis();
    if (LED_RED_timer - time3 < 100)
    {
      digitalWrite(LED_PIN_RED, LOW);
    }
        else if((LED_RED_timer - time3) >= 100 && (LED_RED_timer - time3) < 1100)
        {
        digitalWrite(LED_PIN_RED, HIGH);
        }
          else if ((LED_RED_timer - time3) >= 1100)
          {
          time3 = millis();
          }
    {
    digitalWrite(LED_PIN_BLUE, HIGH);
    LED_BLUE_timer = millis();
    if ((LED_BLUE_timer - time1) < 50)
    {
      digitalWrite(LED_PIN_BLUE, LOW);
    }
      else if ((LED_BLUE_timer - time1) >= 50 && (LED_BLUE_timer - time1) < 250)
      {
        digitalWrite(LED_PIN_BLUE, HIGH);
      }
        else if ((LED_BLUE_timer - time1) >= 250)
        {
          time1 = millis();
        }
    } 
    {
    digitalWrite(LED_PIN_YELLOW, HIGH);
    LED_YELLOW_timer = millis();
    if (LED_YELLOW_timer - time2 < 10)
    {
      digitalWrite(LED_PIN_YELLOW, LOW);
    }
      else if ((LED_YELLOW_timer - time2) >= 10 && (LED_YELLOW_timer - time2) < 30)
      {
        digitalWrite(LED_PIN_YELLOW, HIGH);
      }
        else if ((LED_YELLOW_timer - time2) >= 30)
        {
          time2 = millis();
        }
    }
    }
}
