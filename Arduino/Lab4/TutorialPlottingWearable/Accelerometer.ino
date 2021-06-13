const int accelX = A2;
const int accelY = A3;
const int accelZ = A4;

void setupAccelSensor(){
  Serial.begin(115200);
  pinMode(accelX, INPUT);
  pinMode(accelY, INPUT);
  pinMode(accelZ, INPUT);
}

void readAccelSensor(){
  ax = analogRead(accelX);
  ay = analogRead(accelY);
  az = analogRead(accelZ);
}
