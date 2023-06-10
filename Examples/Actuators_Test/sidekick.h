#pragma once

// ------Internals----
#include "actuators.h"
#include "orientation.h"
#include "sensors.h"
#include "sidekick_state.h"
#include "time_handler.h"
// ------Internals----

Timer sk_timer = Timer();
SideKickState<> state_info = SideKickState<>();
void SideKick() {
    Serial.begin(115200);
    actuators::init();
    sensors::init();
}
