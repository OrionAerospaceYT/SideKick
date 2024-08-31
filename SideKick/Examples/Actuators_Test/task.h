#pragma once

// -----Internals------
#include "sensors.h"
#include "actuators.h"
#include "sub_task.h"
#include "utility.h"
#include "control.h"
#include "time_handler.h"
// -----Internals------

#include "orientation.h"

// Tasks go here-- this keeps the main file clean and focused on the "flow" of tasks
// Our general functions will be defined here things like our main loops
// Long sections of code or repeated code loops can be moved to sub_task.h

// The functions in place here can be changed to suit your needs
// The ones listed here serve as inspiration--feel free to change them as
// you need -- but remember to change your Tasks in main.h

namespace task {

    // Globals can be defined here
    // Can be used for code that only runs once
    // This can also be run multiple times by changing the code flow in main.h
    void Setup() {
      String inputString = "";
    }

    // Can be used to automatically test actuators
    // Very useful for quick plug and play testing
    void ActuatorTest() {}

    // Can be used to print sensor values and any other required calibration
    void Calibration() {}

    // Code that loops
    void Loop() {
      while (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        int dividerIndex = command.indexOf('-');

        if (command.startsWith("reset")) {

          actuators::reset();
          PRINTLN("Reset all actuators.");

        } else if (command.startsWith("addServo")) {

          String servoNumberString = command.substring(dividerIndex + 1);
          actuators::addServo(servoNumberString);

        } else if (command.startsWith("servo")) {

          String servoName = command.substring(0, dividerIndex);
          String servoNumberString = command.substring(dividerIndex + 1);
          int servoNumber = servoNumberString.toInt();

          String indexString = servoName.substring(5);
          int servoIndex = indexString.toInt();
          actuators::moveServo(servoIndex, servoNumber);

        } else if (command.startsWith("addPin")) {

          String pinNumberString = command.substring(dividerIndex + 1);
          int pinNumber = pinNumberString.toInt();
          actuators::addPin(pinNumber);

        } else if (command.startsWith("pin")) {
          String pinName = command.substring(0, dividerIndex);
          String pinNumberString = command.substring(dividerIndex + 1);
          int pinNumber = pinNumberString.toInt();

          String indexString = pinName.substring(5);
          int pinIndex = indexString.toInt();
          actuators::movePin(pinIndex, pinNumber);
        } else {
          PRINTLN("Invalid command.");
        }
      }
    }

}  // namespace task
