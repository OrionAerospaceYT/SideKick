#pragma once

//Simple controller definitions 

//PID controller
template<typename T = float>
struct PID{
T kp;
T ki;
T kd;
T setpoint;
T integral_err;
T previous_err;
T min_lim;
T max_lim;
bool lims_set = false;

PID(T p_gain, T i_gain, T d_gain, T setpoint = 0) : kp(p_gain), ki(i_gain), kd(d_gain), setpoint(setpoint){}

void setlims(T min, T max){
	min_lim = min;
	max_lim = max;
	lims_set = true;
}
void setSetpoint(T new_setpoint){
	setpoint = new_setpoint;
}
T update(T input, T dt){
	auto error = setpoint - input;
	
	//assert dt must not be 0
	auto derivative_err = (error - previous_err) / dt;
	
	integral_err += error * dt;

	auto output = kp*error + ki*integral_err + kd*derivative_err;

	previous_err = error;

	if(lims_set){
		if(output > max_lim){
			output = max_lim;	
		}
		else if(output < min_lim){
			output = min_lim;
		}
	}
	return output;
}

};
