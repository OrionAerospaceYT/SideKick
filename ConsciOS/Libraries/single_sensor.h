#pragma once 

#include "common.h"

enum pintype{ANALOG,DIGITAL};
struct SingleDataPointSensor{
	bool read_type;
	int pin; 
	SingleDataPointSensor(int pin, bool pin_type){
		read_type = pin_type;
		this->pin = pin;
		pinMode(pin,INPUT);
	}
	void init(int pin, bool pin_type){
		read_type = pin_type;
		this->pin = pin;
		pinMode(pin,INPUT);
	}
	int read(){
		return read_type ? digitalRead(pin) : analogRead(pin);
	}

};

	









