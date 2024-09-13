/*
    Controlling multiple steppers with the AccelStepper and MultiStepper library

     by Dejan, https://howtomechatronics.com
*/

#include <AccelStepper.h>
#include <MultiStepper.h>

// Define the stepper motor and the pins that is connected to
AccelStepper stepper1(1, 2, 3); // (Typeof driver: with 2 pins, STEP, DIR)
AccelStepper stepper2(1, 4, 5);

MultiStepper steppersControl;  // Create instance of MultiStepper

long gotoposition[3]; // An array to store the target positions for each stepper motor

void setup() {
  Serial.begin(9600);
  // config motors
  stepper1.setMaxSpeed(600);
  stepper1.setAcceleration(4000);
  stepper1.setCurrentPosition(0);  
  
  stepper2.setMaxSpeed(600);
  stepper2.setAcceleration(4000);
  stepper2.setCurrentPosition(0);  

  // Adding the 3 steppers to the steppersControl instance for multi stepper control
  steppersControl.addStepper(stepper1);
  steppersControl.addStepper(stepper2);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string
    String command = Serial.readStringUntil('\n');

    // Execute the command
    executeCommand(command);
  }
}


void executeCommand(String cmd) {
  // Print the received command for debugging
  Serial.print("Received command: ");
  Serial.println(cmd);

  // Split the command into parts
  int firstSpaceIndex = cmd.indexOf(' ');
  String commandName;
  String arguments;

  if (firstSpaceIndex == -1) {
    commandName = cmd;
    arguments = "";
  } else {
    commandName = cmd.substring(0, firstSpaceIndex);
    arguments = cmd.substring(firstSpaceIndex + 1);
  }

  // Print command name and arguments for debugging
  Serial.print("Command name: ");
  Serial.println(commandName);
  Serial.print("Arguments: ");
  Serial.println(arguments);

  // Split arguments into an array of integers
  int argArray[10]; // Array to hold up to 10 integer arguments
  int argCount = 0;
  int lastIndex = 0;

  while (lastIndex < arguments.length() && argCount < 10) {
    int spaceIndex = arguments.indexOf(' ', lastIndex);
    if (spaceIndex == -1) {
      spaceIndex = arguments.length();
    }
    String argStr = arguments.substring(lastIndex, spaceIndex);
    argArray[argCount] = argStr.toInt();
    argCount++;
    lastIndex = spaceIndex + 1;
  }

  // Handle the command
  if (commandName == "M1") { // Example command to turn LED on
    Serial.println("LED is turned ON.");
  } else if (commandName == "M0") { // Example command to turn LED off
    Serial.println("LED is turned OFF.");
  } else if (commandName == "G1") {
    // Example G1 command handling
    Serial.print("G1 command received with ");
    Serial.print(argCount);
    Serial.println(" arguments.");
    gotoposition[0] = argArray[0];
    gotoposition[1] = argArray[1];
  
    steppersControl.moveTo(gotoposition);
    steppersControl.runSpeedToPosition();
  } else {
    Serial.println("Unknown command.");
  }
}
