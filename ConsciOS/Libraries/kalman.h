#pragma once 

#include "common.h"
#include "SKmath.h"
#include "./External/BasicLinearAlgebra.h"
//L = dimension of input vector, M = dimension of measured vector, N = dimension of state vector
//Add a warning that if the thing is only 1x1 that using the singlekf located in skmath would be easier 
template <int L, int M, int N>
class Kalman{
	public:
	BLA::Matrix<N,N> A; //State Space dynamics matrix
	BLA::Matrix<N,L> B; //State Space input dynamics matrix
	BLA::Matrix<M,N> C; //State Space output matrix
	BLA::Matrix<N,M> K; //Kalman gain
	BLA::Matrix<N,N> I; //Identity matrix
	BLA::Matrix<N,N> P; //estimate covariance matrix
	BLA::Matrix<N,N> Q; //Dynamics covariance
	BLA::Matrix<M,M> R; //Measurement covariance
	BLA::Matrix<M,M> S; //Innovation covariance
	BLA::Matrix<L> u; //input vector (control input)
	BLA::Matrix<M> y; //measurement vector (sensor etc input)
	BLA::Matrix<M> q_pred; //predicted state
	BLA::Matrix<N> q_est; //estimated state vector
	Kalman(){}
	

	void updateState(const BLA::Matrix<L> &u, const BLA::Matrix<M> &y){
		this->u = u;
		this->y = y;
		predict();
		correct();
	}

	private:

	void predict(){
		q_pred = A * q_est + B * u;
		auto A_T = ~A;
		P = A * P * A_T + Q;
	}
	
	void correct(){
		auto C_T = ~C;
		S = C * P * C_T + R;
		auto S_I = S;
		K = P * C_T * BLA::Invert(S_I);
		q_est = q_pred + K * (y - C * q_pred);
		P = (I - K * C) * P;
	}

};
