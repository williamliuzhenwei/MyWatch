const int accelX = A0;
void setup() {
  Serial.begin(9600);
  pinMode(accelX, INPUT);


}

void loop() {
  int accel_val = analogRead(accelX);
  Serial.println(accel_val);
}
