#define COIL1 4
#define COIL2 5
#define COIL3 6
#define COIL4 7
#define MOTOR_ENABLE 8
#define AC A1
#define DC A0
#define BT_CONNECTED 2
#define BT_ENABLE 3
#define SAMPLING_RATE_HZ 200

#define FORWARD_DIR -1

#define AD_PER_STEP 10
#define AD_DELAY 10

int motor_state = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(COIL1, OUTPUT);
  pinMode(COIL2, OUTPUT);
  pinMode(COIL3, OUTPUT);
  pinMode(COIL4, OUTPUT);
  pinMode(MOTOR_ENABLE, OUTPUT);
  pinMode(BT_ENABLE, OUTPUT);
  pinMode(BT_CONNECTED, INPUT);
  digitalWrite(3, HIGH);
  
  Serial.begin(19200);
  delay(100);
  Serial.write("AT+RICD+\r");
  Serial.flush();
}

void loop() {
  if(digitalRead(2) == LOW) {
    checkForCommands();
    static int last_sent = millis();
    if((millis() - last_sent) >= (1000/SAMPLING_RATE_HZ)) {
      sendACDCVoltages();
      last_sent = millis();
    }
  }
}

void checkForCommands() {
  if(Serial.available()) {
    char command = Serial.read();
    switch(command) {
      case 'f':
        takeStep(FORWARD_DIR);
        break;
      case 'r':
        takeStep(-FORWARD_DIR);
        break;
      case 'e':
        digitalWrite(MOTOR_ENABLE, HIGH);
        break;
      case 'd':
        digitalWrite(MOTOR_ENABLE, LOW);
        break;
      default:
        break;
    }
  }
}

void sendACDCVoltages() {
  int ac_voltage = analogRead(AC);
  int dc_voltage = analogRead(DC);
  Serial.write("AC");
  Serial.write(ac_voltage);
  Serial.write("DC");
  Serial.write(dc_voltage);
  Serial.flush();
}

void takeStep(int direction) {
  for(int counter = 0; counter < AD_PER_STEP; counter++) {
    advanceMotor(direction);
    delay(AD_DELAY);
  }
  allOff();
}

void allOff() {
  digitalWrite(COIL1, LOW);
  digitalWrite(COIL2, LOW);
  digitalWrite(COIL3, LOW);
  digitalWrite(COIL4, LOW);  
}

void advanceMotor(int direction) {
  allOff();
  if((motor_state + direction) < 0) {
    motor_state = 3;
  } else {
    motor_state = (motor_state + direction) % 4; 
  }
  switch (motor_state) {
    case 0:
      digitalWrite(COIL1, HIGH);
      break;
    case 1:
      digitalWrite(COIL3, HIGH);
      break;
    case 2:
      digitalWrite(COIL2, HIGH);
      break;
    case 3:
      digitalWrite(COIL4, HIGH);
      break;
  }
}
