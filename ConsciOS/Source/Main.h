#pragma once


//-----Internals------
#include "./libraries/common.h"
#include "task.h"
#include "sidekick.h"
//-----Internals------

namespace sm{

	//These are the set of tasks our robot will complete (Note: this does not specify the order)
	//You can change the Tasks in here, but make sure to follow the naming convention
	enum Task{Setup,ActuatorTest,Calibration,Loop};

	//This is where the "flow" of tasks is defined
	//Task functions are defined in "task.h"
	void TaskFlow(Task current_task){
		switch (current_task) {
		  case Setup:
		  task::Setup();
		  state_info.current_task = ActuatorTest; //Using lines like this we can control the "flow" of tasks
		  break;
		  case ActuatorTest:
		  task::ActuatorTest();
		  state_info.current_task = Calibration;
		  break;
		  case Calibration:
		  task::Calibration();
		  state_info.current_task = Loop;
		  break;
		  case Loop:
		  task::Loop();
		  break;
		}
	}



	//------INTERNAL-----
	// DO NOT TOUCH
	void SM_UPDATE_LOOP(){
		TaskFlow(state_info.current_task);
		END_LOG;
	}

	void SM_INIT(){
		SideKick();
	}
//------INTERNAL-----
}//ns sm
