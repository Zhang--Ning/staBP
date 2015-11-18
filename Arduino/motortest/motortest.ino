#define COIL1 2
#define COIL2 3
#define COIL3 4
#define COIL4 5
#define AD_PER_STEP 10
#define AD_DELAY 10
#define MOTOR_POSITION_MAX 100
#define FORWARD_DIR -1
#define DISENGAGE_TIME 9000

int motor_position = 0;
int motor_state = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(COIL1, OUTPUT);
  pinMode(COIL2, OUTPUT);
  pinMode(COIL3, OUTPUT);
  pinMode(COIL4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while(Serial.available()) {
    char user_input = Serial.read();
    switch(user_input) {
      case 'f':
        motorIncrease();
        break;
      case 'r':
        motorDecrease();
        break;
      case 'q':
        motorDisengage();
        break;
      case 'p':
        Serial.print("Position: ");
        Serial.println(motor_position);
        break;
      default:
        break;
    }
  }
}

void motorIncrease() {
  takeStep(FORWARD_DIR);
  motor_position++;  
}

void motorDecrease() {
  takeStep(-FORWARD_DIR);
  motor_position--;
}

void motorDisengage() {
  int time_start = millis();
  while((millis()-time_start) < DISENGAGE_TIME) {
    motorDecrease();
    Serial.println("Backing up...");
  }
  motor_position = 0;
}

void motorSetPosition(int goal_position) {
  int delta = motor_position - goal_position;
  while(delta != 0) {
    if(delta < 0) {
      motorIncrease();
    } else {
      motorDecrease();
    }
  }
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
 
