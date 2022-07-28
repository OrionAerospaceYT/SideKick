#pragma once

#include "common.h"
#include <Wire.h>

struct Timer{
uint32_t cycles = 0;
uint32_t start_t = 0;
uint32_t finish_t = 0;
float delta_t = 0;

Timer(){}
void start(){start_t = micros();}
void stop(){finish_t = micros();}
float deltaT(){
if(finish_t == 0){stop();}
return (finish_t - start_t) / 1000000.0f; }
void count(){cycles++;}
uint32_t getCycles(){return cycles;}
float getTime(){return start_t / 1000000.0f;}
};
