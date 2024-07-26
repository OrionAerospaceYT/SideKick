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
#define DEG2RAD 3.14159265358979323846264343383/180

// The functions in place here can be changed to suit your needs
// The ones listed here serve as inspiration--feel free to change them as
// you need -- but remember to change your Tasks in main.h

namespace task {

    unsigned long counter = 0;

    // Globals can be defined here
    // Can be used for code that only runs once
    // This can also be run multiple times by changing the code flow in main.h
    void Setup() {
        PRINTLN("Setting up your board...");
        delay(200);
    }

    // Can be used to automatically test actuators
    // Very useful for quick plug and play testing
    void ActuatorTest() {
      PRINTLN("Testing Actuators...");
      delay(200);
    }

    // Can be used to print sensor values and any other required calibration
    void Calibration() {
      PRINTLN("Calibrating Actuators...");
      delay(200);
      PRINTLN("Done!");
      delay(200);
    }

    // Code that loops
    void Loop() {
      // Increment counter
      counter++;

      // Graph sin(x) and a step function on the top graph
      GRAPH("Sin(x)",sin(counter*DEG2RAD),TOP);
      GRAPH("Step", sin(counter*DEG2RAD) + sin(counter*DEG2RAD*3)/6,TOP)

      // Graph tan(x) on the bottom graph
      //if ((counter + 90) % 180 != 0){
        GRAPH("Tan(x)",tan(counter*DEG2RAD),BOT);
      //} else {
      //  GRAPH("Tan(x)",0,BOT);
      //}

      // Print the counter's value
      PRINT("This is loop " + String(counter));
      END_LOG;

      // Add a small delay between loops
      delay(30);
    }

    void Loop2() {

    }

}  // namespace task
