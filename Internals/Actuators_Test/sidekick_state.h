#pragma once

#include "utility.h"
#include "vector.h"

template <typename T = float>
struct SideKickState {
    Vec ypr;        // yaw pitch roll
    Vec ypr_rate;   // yaw pitch roll rates
    Vec ypr_accel;  // yaw pitch roll angular acceleration
    Vec xyz_br;     // body relative position
    Vec vel_br;     // body relative axis rates
    Vec accel_br;   // body relative axis accelerations
    int current_task;
    uint32_t current_task_time;
};
