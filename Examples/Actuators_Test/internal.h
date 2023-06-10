#pragma once

//-----Internals------
#include "utility.h"
#include "sidekick.h"
#include "task_flow.h"
//-----Internals------

namespace sm {
//------INTERNAL-----
// DO NOT TOUCH
void SM_UPDATE_LOOP() {
    taskSchedule();
    END_LOG;
}

void SM_INIT() {
    SideKick();
    taskInit();
}
//------INTERNAL-----
}  // namespace sm
