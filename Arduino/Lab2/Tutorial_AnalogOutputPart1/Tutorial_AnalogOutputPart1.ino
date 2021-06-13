const int pwmFrequency = 5000;  // Set the PWM frequency to 5KHz
const int pwmChannel = 0;       // Use PWM channel 0
const int pwmBitResolution = 8; // Set a PWM resolution of 8-bits
void setup() {
    ledcSetup (pwmChannel, pwmFrequency, pwmBitResolution);
    ledcAttachPin(LED_BUILTIN, pwmChannel);


}

void loop() {
  ledcWrite(pwmChannel, 0);
     delay(2000);
     ledcWrite(pwmChannel,127);
     delay(2000);
     ledcWrite(pwmChannel, 255);
     delay(2000);
     ledcWrite(pwmChannel, 90);
     delay(2000);
}
