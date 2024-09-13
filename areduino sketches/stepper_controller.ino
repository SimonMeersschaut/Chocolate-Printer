#include <AccelStepper.h>

// Define the stepper motor and the pins that is connected to
AccelStepper stepper1(1, 3, 4); // (Type of driver: with 2 pins, STEP, DIR)

bool dir = false;

void setup() {
  Serial.begin(9600);
  // Set maximum speed value for the stepper
  stepper1.setMaxSpeed(600);
  stepper1.setAcceleration(4000);
  if (dir){
    stepper1.setCurrentPosition(800);  
  }
  else{
    stepper1.setCurrentPosition(0);  
  }
  
  
}

void loop() {
  Serial.println("ok");
  
  if (dir){
    stepper1.moveTo(0);
    while (stepper1.currentPosition() != 0) {
      stepper1.run();  // Move or step the motor implementing accelerations and decelerations to achieve the target position. Non-blocking function
    }
  }else{
    stepper1.moveTo(800);
    while (stepper1.currentPosition() != 800) {
      stepper1.run();  // Move or step the motor implementing accelerations and decelerations to achieve the target position. Non-blocking function
    }
  }
  
  
}
