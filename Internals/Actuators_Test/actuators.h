#pragma once

//-----Internals------

#include "actuator_struct.h"
#include "utility.h"
//#include "internal_defs.h"

//-----Internals------

// Include your Actuator libraries here
#include <Servo.h>

//Include your Actuator libraries here

namespace actuators{

  // Globals can be defined here
  const int MAX_NUM_OF_SERVOS = 128;
  Servo servos[MAX_NUM_OF_SERVOS];
  int positions[MAX_NUM_OF_SERVOS];
  int servoCount = 0;

  void init()
  {
  }

  void reset() {
    Servo servos[MAX_NUM_OF_SERVOS];
    int positions[MAX_NUM_OF_SERVOS];
    int servoCount = 0;
  }

  void addServo(int pin) {
    if (servoCount < MAX_SERVOS) {
      servos[servoCount].attach(pin);  // attach a new Servo object to the specified pin
      servoCount++;  // increment the number of servos
      PRINT("Added new servo at pin ");
      PRINT(pin);
    } else {
      PRINT("Cannot add more servos!");
    }
  }

  void moveServo(int servoIndex, int pos) {
    if (servoIndex < servoCount) {
      servos[servoIndex].write(pos);  // move the specified servo to the desired position
      PRINT("Moved servo ");
      PRINT(servoIndex);
      PRINT(" to position ");
      PRINT(pos);
    } else {
      PRINT("Invalid servo index!");
    }
    positions[servoIndex] = pos;
  }
}  // namespace actuators
