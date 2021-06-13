void setup() {
  setupCommunication();
  setupDisplay();
}

void loop() {
  String message = receiveMessage();
  if(message != "") {
    writeDisplayCSV(message, 2);
    sendMessage(message);
  }
}
