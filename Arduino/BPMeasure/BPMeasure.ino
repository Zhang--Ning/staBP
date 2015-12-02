#define COIL1 2
#define COIL2 3
#define COIL3 4
#define COIL4 5
#define PRESSURE_SENSOR 6
#define AD_PER_STEP 10
#define AD_DELAY 10
#define DISENGAGE_TIME 2000
#define MOTOR_POSITION_MAX 100
#define CALIBRATION_INTERVAL 1200
#define SAMPLING_RATE 2000
#define CREST_TIME 2
#define FORWARD_DIR 1
#define ENGAGE_PRESSURE_THRESHOLD 1000

char user_input;
int motor_position = 0;
int motor_state = 0;
int last_calibration = -1;

void setup() {
  // put your setup code here, to run once:
  pinMode(COIL1, OUTPUT);
  pinMode(COIL2, OUTPUT);
  pinMode(COIL3, OUTPUT);
  pinMode(COIL4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(shouldCalibrate()) {
    calibrate();
  } else {
    Serial.write(readPressure());
    delay(1000/SAMPLING_RATE);
  }
}

int readPressure() {
  return analogRead(PRESSURE_SENSOR);
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
  }
  motor_position = 0;
}

void motorEngage() {
  while(readPressure() < ENGAGE_PRESSURE_THRESHOLD) {
    motorIncrease();  
  }
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

int getCrest() {
  int wave[CREST_TIME*SAMPLING_RATE];
  for(int i = 0; i < CREST_TIME*SAMPLING_RATE; i++) {
    wave[i] = readPressure();
    delay(1000/SAMPLING_RATE);
  }
  int crest = getWavePeakAmp(wave)/getWaveRMS(wave);
  return crest;
}

int getWaveRMS(int* wave) {
  int sum = 0;
  for(int i = 0; i < CREST_TIME*SAMPLING_RATE; i++) {
    sum += wave[i]^2;
  }
  return sqrt(sum/CREST_TIME*SAMPLING_RATE);
}

int getWavePeakAmp(int* wave) {
  int maximum = wave[0];
  int minimum = wave[0];
  for(int i = 0; i < CREST_TIME*SAMPLING_RATE; i++) {
    if(wave[i] > maximum) {
      maximum = wave[i];
    }
    if(wave[i] < minimum) {
      minimum = wave[i];
    }
  }
  return maximum-minimum;
}

int getHoldingPosition() {
  motorDisengage();
  motorEngage();
  int numSteps = MOTOR_POSITION_MAX-motor_position;
  int maxCrest = 0;
  int maxPosition = motor_position;
  for(int i = 0; i < numSteps; i++) {
    int crest = getCrest();
    if(crest > maxCrest) {
      maxCrest = crest;
      maxPosition = motor_position;
    }
    motorIncrease();
  }
  return maxPosition;
}

void calibrate() {
  int holding_position = getHoldingPosition();
  motorSetPosition(holding_position);
  last_calibration = millis()/1000;
}

bool shouldCalibrate() {
  return (last_calibration == -1) ||
      (((millis()/1000)-last_calibration) > CALIBRATION_INTERVAL);
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
