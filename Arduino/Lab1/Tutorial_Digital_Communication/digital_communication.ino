const int BUTTON_PIN = 14;
const int LED_PIN = 13;
void setup()
{
     pinMode(LED_BUILTIN, OUTPUT);
     pinMode(BUTTON_PIN, INPUT);
     pinMode(LED_PIN, OUTPUT);
}


void loop() {
// Blinking LED
/*
     digitalWrite(LED_BUILTIN, HIGH);
     delay(500);
     digitalWrite(LED_BUILTIN, LOW);
     delay(1000); */

// Digital Read & button
/*
     if (digitalRead(BUTTON_PIN) == LOW) {
         digitalWrite(LED_BUILTIN, HIGH);     
     }
     else {
          digitalWrite(LED_BUILTIN, LOW); */

// Digital Write & LEDs
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);
    delay(1000); 




}
