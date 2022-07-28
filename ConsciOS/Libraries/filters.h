#pragma once 

//Simple filter definitions 

//Kalman filter for single data point/1dof systems
//A lower Q value means more agressive filtering, R is the covariance of the sensor
template <typename T = float>
struct SingleKalman{
T Q = 0;
T R = 0;
T A = 1;
T B = 0;
T C = 1;
T D = 0;
T x_hat = 0;
T P = 0;
SingleKalman(T q, T r) : Q(q), R(r){}
void setB(T b){B = b;}

T filter(T Y, T U = 0){
  auto x_hat_new = A * x_hat + B * U;
  P = A * P * A + Q;
  auto K = P * C * (T(1) / (C * P * C + R));
  x_hat_new += K * (Y - C * x_hat_new);
  P = (T(1) - K * C) * P;
  x_hat = x_hat_new;
  return x_hat;
}

};


//First Order IIR lowpass filter 
//Given alpha (filter coeffecient)
template <typename T = float> 
struct LowPassFilter{
T previous_output = 0;
T alpha;
LowPassFilter(T a) : alpha(a){}
T filter(T signal){
	auto out = alpha*previous_output + (T(1) - alpha) * signal;
	previous_output = out;
	return out;
}
};
