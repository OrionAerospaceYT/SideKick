#pragma once

//-----Internals------
#include "utility.h"
#include "array.h"
#include "transition_map.h"
#include "task.h"
//-----Internals------

// You can change the Tasks in here, but make sure to follow the naming convention
// These are the set of tasks our robot will complete
//(Note: this does not specify the order)
const int TASK_COUNT = 4;
enum Task
{
    Setup,
    ActuatorTest,
    Calibration,
    Loop
};
Array<taskFunc, TASK_COUNT> TaskFlow(task::Setup, task::ActuatorTest, task::Calibration,
 task::Loop);
TransitionMap<TASK_COUNT> transition_map(TaskFlow);

void taskInit()
{
    transition_map.setDefaultState(Setup);
}

void taskSchedule()
{
    // to add transitions to the states follow the format below
    // transition_map.add(starting state, exit condition (evaluatable bool),exit state);
    transition_map.add(Setup, LOOP_ONCE, ActuatorTest);
    transition_map.add(ActuatorTest, LOOP_ONCE, Calibration);
    transition_map.add(Calibration, LOOP_ONCE, Loop);

}
