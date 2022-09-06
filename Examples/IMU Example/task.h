#pragma once

//-----Internals------
#include "sensors.h"
#include "actuators.h"
#include "sub_task.h"
#include "common.h"
#include "sidekick.h"
//-----Internals------

//Tasks go here-- this keeps the main file clean and focused on the "flow" of tasks
//Our general functions will be defined here things like our main loops
//Long sections of code or repeated code loops can be moved to sub_task.h

//The functions in place here can be changed to suit your needs
//The ones listed here serve as inspiration--feel free to change them as you need -- but remember to change your Tasks in main.h
namespace task{

	//Globals can be defined here
	Timer timer;
	float dt;

	//Can be used for code that only runs once
	//This can also be run multiple times by changing the code flow in main.h
	void Setup(){
		sensors::init();
		timer.start();
	}

	//Can be used to automatically test actuators
	//Very useful for quick plug and play testing
	void ActuatorTest(){

	}

	//Can be used to print sensor values and any other required calibration
	void Calibration(){

	}

	//Code that loops
	void Loop(){
		dt = timer.deltaT();
		timer.start();

		sensors::update(state_info.ypr_rate, state_info.ypr, dt);

		TOP_GRAPH("X Ori", state_info.ypr.x)
		TOP_GRAPH("Y Ori", state_info.ypr.y)
		TOP_GRAPH("Z Ori", state_info.ypr.z)

		BOTTOM_GRAPH("X Rate", state_info.ypr_rate.x)
		BOTTOM_GRAPH("Y Rate", state_info.ypr_rate.y)
		BOTTOM_GRAPH("Z Rate", state_info.ypr_rate.z)

		PRINT(dt)

		timer.stop();
	}

}
