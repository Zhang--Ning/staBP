int AC_pin = A7;
int DC_pin = A6;
void setup() {
  Serial.begin(115200);
}

void loop() {
  // read the value from the sensor:
  Serial.println(analogRead(AC_pin));
  Serial.println(analogRead(DC_pin));
  delay(5);
}
