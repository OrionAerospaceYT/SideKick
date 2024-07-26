#pragma once

// -----Internals------
#include "actuator_struct.h"
#include "utility.h"
// -----Internals------

// Include your Actuator libraries here
#include <Servo.h>

#ifdef ARDUINO_ARCH_RP2040
#include "stem.h"
#include "skServo.h"

namespace actuators {

  // Globals can be defined here
  const int MAX_NUM_OF_SERVOS = 128;

  int servo_count = 0;
  int gpio_count = 0;
  int stem_count = 0;

  int servo_pins[MAX_NUM_OF_SERVOS];
  Servo servos[MAX_NUM_OF_SERVOS];
  skServo* stemServos[] = {&stem::S1, &stem::S2, &stem::S3, &stem::S4,
                        &stem::S5, &stem::S6, &stem::S7, &stem::S8,
                        &stem::S9, &stem::S10, &stem::S11, &stem::S12};

  const int MAX_NUM_OF_PINS = 128;
  int pins[MAX_NUM_OF_PINS];
  int pin_count = 0;

  void init()
  {
  }

  void reset() {
    for (int i=0; i<MAX_NUM_OF_SERVOS; i++){
      servos[i].detach();
    }
    servo_count = 0;
    pin_count = 0;
  }

  void addServo(String pinStr) {
    int pin;
    if (pinStr.substring(0,1) == "S"){
      pin = -pinStr.substring(1,3).toInt();
    } else {
      pin = pinStr.toInt();
    }

    if (servo_count < MAX_NUM_OF_SERVOS) {
      if (pin >= 0){
        servo_pins[servo_count] = gpio_count;
        servos[gpio_count].attach(pin);  // attach a new Servo object to the specified pin
        gpio_count ++;
      } else {
        PRINTLN("Stem Servo");
        servo_pins[servo_count] = pin;
        stem_count ++;
      }
      servo_count++;  // increment the number of servos
      PRINT("Added new servo at pin ");
      PRINTLN(pinStr);
    } else {
      PRINTLN("Cannot add more servos!");
    }
  }

  void moveServo(int pinIndex, int pos) {
    if (pinIndex < servo_count){
      int pin = servo_pins[pinIndex];
      if (pin >= 0) {
        servos[pin].write(pos);  // move the specified servo to the desired position
        PRINT("Moved servo ");
        PRINT(pinIndex);
        PRINT(" to position ");
        PRINTLN(pos);
      } else {
        pin = -pin - 1;
        PRINTLN("Moved STEM pin S" + String(pin+1) + " to position " + String(pos));
        stemServos[pin]->write(pos);
      }
    } else {
      PRINTLN("Invalid servo index!");
    }
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
  }

}  // namespace actuators

#else

namespace actuators {

  // Globals can be defined here
  const int MAX_NUM_OF_SERVOS = 128;
  Servo servos[MAX_NUM_OF_SERVOS];
  int servo_count = 0;

  const int MAX_NUM_OF_PINS = 128;
  int pins[MAX_NUM_OF_PINS];
  int pin_count = 0;

  void init()
  {
  }

  void reset() {
    for (int i=0; i<MAX_NUM_OF_SERVOS; i++){
      servos[i].detach();
    }
    servo_count = 0;
    pin_count = 0;
  }

  void addServo(String pinStr) {
    int pin = pinStr.toInt();
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
  }
}  // namespace actuators

#endif
