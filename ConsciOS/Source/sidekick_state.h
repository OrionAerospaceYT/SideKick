#pragma once

#include "./libraries/common.h"
#include "./libraries/vector.h"



template <typename T = float>
struct SideKickState {
	Vec<T> ypr;//yaw pitch roll 
	Vec<T> ypr_rate;// yaw pitch roll rates
	Vec<T> ypr_accel;//yaw pitch roll angular acceleration
	Vec<T> xyz_br; //body relative position 
	Vec<T> vel_br; //body relative axis rates
	Vec<T> accel_br; //body relative axis accelerations
	int current_task;
};




