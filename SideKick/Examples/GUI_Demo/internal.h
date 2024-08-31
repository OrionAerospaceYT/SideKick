#pragma once

// -----Internals------
#include "utility.h"
#include "task_flow.h"
#include "time_handler.h"
#include "sidekick_state.h"
// Stem include wrapper 
// NOTE: Not robust for regualr pico compiles
#ifdef ARDUINO_ARCH_RP2040
#include "stem.h"
#include "skServo.h"
// -----Internals------


namespace sm {
// ------INTERNAL-----
// DO NOT TOUCH
void SM_UPDATE_LOOP() {
    taskSchedule();
}


void SM_INIT() {
    Serial.begin(115200);
    // Wait for Gui connection
    while (!Serial) {}
    taskInit();
    sk_internal_bus.begin();
    stem::S1.attach(PS1);
    stem::S2.attach(PS2);
    stem::S3.attach(PS3);
    stem::S4.attach(PS4);
    stem::S5.attach(PS5);
    stem::S6.attach(PS6);
    stem::S7.attach(PS7);
    stem::S8.attach(PS8);
    stem::S9.attach(PS9);
    stem::S10.attach(PS10);
    stem::S11.attach(PS11);
    stem::S12.attach(PS12);
}
// ------INTERNAL-----
#else

namespace sm {
// DO NOT TOUCH
void SM_UPDATE_LOOP() {
    taskSchedule();
}

void SM_INIT() {
    Serial.begin(115200);
    // Wait for Gui connection
    while (!Serial) {}
    taskInit();
}
#endif
}  // namespace sm
