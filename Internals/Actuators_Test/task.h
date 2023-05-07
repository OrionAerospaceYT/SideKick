#pragma once

//-----Internals------
#include "sensors.h"
#include "actuators.h"
#include "sub_task.h"
#include "utility.h"
#include "sidekick.h"
//-----Internals------

// Tasks go here-- this keeps the main file clean and focused on the "flow" of tasks
// Our general functions will be defined here things like our main loops
// Long sections of code or repeated code loops can be moved to sub_task.h

// The functions in place here can be changed to suit your needs
// The ones listed here serve as inspiration--feel free to change them as you need -- but remember to change your Tasks in main.h
namespace task
{

    // Globals can be defined here
    String inputString = "";

    // Can be used for code that only runs once
    // This can also be run multiple times by changing the code flow in main.h
    void Setup(){
        subtask::exampleLongFunc(); // you can delete this purely for demonstration
    }

    // Can be used to automatically test actuators
    // Very useful for quick plug and play testing
    void ActuatorTest(){
    }

    // Can be used to print sensor values and any other required calibration
    void Calibration(){
    }

    // Code that loops
    void Loop()
    {
      while (Serial.available()) {
        String command = Serial.readStringUntil('\n');

        if (command.startsWith("reset")) {
          actuators::reset();
        }

        int dividerIndex = command.indexOf('-');

        if (dividerIndex != -1) {
          String servoName = command.substring(0, dividerIndex);
          String servoNumberString = command.substring(dividerIndex + 1);
          int servoNumber = servoNumberString.toInt();

          if (servoName.startsWith("addservo")) {
            actuators::addServo(servoNumber);
          }
          if (servoName.startsWith("servo")) {
            String indexString = servoName.substring(5);
            int servoIndex = indexString.toInt();
            actuators::moveServo(servoIndex, servoNumber);
          }
        }
      }

      /*for (int i=0; i<actuators::servoCount; i++)
      {
        GRAPH(i, actuators::positions[i], TOP);
      }*/
    }

} // namespace task
