#pragma once 

//------Internals----
#include "./libraries/time_handler.h"
#include "sidekick_state.h"
#include "./libraries/orientation.h"
//------Internals----

Timer sk_timer = Timer();
SideKickState<> state_info = SideKickState<>();
Orientation ori = Orientation(state_info.ypr);
void SideKick(){
Serial.begin(9600);
actuators::init();
sensors::init();
}

