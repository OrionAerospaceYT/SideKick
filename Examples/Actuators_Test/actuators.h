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
  int servo_positions[MAX_NUM_OF_SERVOS];
  int servo_count = 0;

  const int MAX_NUM_OF_PINS = 128;
  int pins[MAX_NUM_OF_PINS];
  int pin_positions[MAX_NUM_OF_PINS];
  int pin_count =0;

  void init()
  {
  }

  void reset() {
    for (int i=0; i<MAX_NUM_OF_SERVOS; i++){
      servos[i].detach();
    }
    servos[MAX_NUM_OF_SERVOS];
    servo_positions[MAX_NUM_OF_SERVOS];
    servo_count = 0;

    pins[MAX_NUM_OF_PINS];
    pin_positions[MAX_NUM_OF_PINS];
    pin_count = 0;
  }

  void addServo(int pin) {
    if (servo_count < MAX_NUM_OF_SERVOS) {
      servos[servo_count].attach(pin);  // attach a new Servo object to the specified pin
      servo_count++;  // increment the number of servos
      PRINT("Added new servo at pin ");
      PRINTLN(pin);
    } else {
      PRINTLN("Cannot add more servos!");
    }
  }

  void moveServo(int servoIndex, int pos) {
    if (servoIndex < servo_count) {
      servos[servoIndex].write(pos);  // move the specified servo to the desired position
      PRINT("Moved servo ");
      PRINT(servoIndex);
      PRINT(" to position ");
      PRINTLN(pos);
    } else {
      PRINTLN("Invalid servo index!");
    }
    servo_positions[servoIndex] = pos;
  }

  void addPin(int pin) {
    if (pin_count < MAX_NUM_OF_PINS) {
      pin_count++;  // increment the number of servos
      PRINT("Added new pin at ");
      PRINTLN(pin);
    } else {
      PRINTLN("Cannot add more servos!");
    }
  }

  void movePin(int pinIndex, int pos) {
    if (pinIndex < pin_count) {
      analogWrite(pins[pinIndex], pos);  // move the specified servo to the desired position
      PRINT("Moved pin ");
      PRINT(pinIndex);
      PRINT(" to position ");
      PRINTLN(pos);
    } else {
      PRINTLN("Invalid servo index!");
    }
    pin_positions[pinIndex] = pos;
  }
}  // namespace actuators
