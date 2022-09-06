#pragma once 

//------Internals----
#include "time_handler.h"
#include "sidekick_state.h"
#include "orientation.h"
#include "actuators.h"
#include "sensors.h"
//------Internals----

Timer sk_timer = Timer();
SideKickState<> state_info = SideKickState<>();
void SideKick(){
Serial.begin(115200);
actuators::init();
sensors::init();
}

