#pragma once 
#include "sk_math.h"
#include "common.h"
#include "quaternion.h"
#include "vector.h"

//THIS NEEDS TO BE CHANGED 
struct Orientation{
	Quat<> base;	
	Vec<>* ypr;
	Orientation(Quat<> base, Vec<> &ypr) : base(base), ypr(&ypr) {}
	Orientation(Vec<> &ypr) : ypr(&ypr) {}
	Orientation() = default;
	~Orientation() = default;
	//purely gyro based orientation resolution
	//this will suffer from gyro drift
	template <typename T, typename F>
	void resolveOrientation(const T &gyro, const F &dt){
		base += base.fromAngularRate(gyro) * dt;  
		base.normalize();
		base.toEulerVector(*(ypr));
	}


	//using gradient descent with accel data and gyro data to give orientation (madgwick paper)
	//FLOAT CASTING ALL THROUGH REEE IS THIS OKAY???
	//also need to look into why accell is not a const
	//we are importing vec and quat so can do a template type T,S etc and make Quat<T> as a passed parameter 
	//this will also allow the typing T to be used to cast the floats used rn 
	template <typename T, typename S, typename F>
	void resolveOrientation(const T &gyro, T &accel, T &ypr, S &base, const F &dt){
		auto qdot = base.fromAngularRate(gyro);
		auto norm = accel.magnitude();
		auto norm_accel = accel / norm;
		auto base_2 = base * 2.0f; 
		auto base_4 = base * 4.0f;
		auto basei_8 = base.i * 8.0f;
		auto basej_8 = base.j * 8.0f;
		auto base_sq = base.squareElements();
		auto s0 = base_4.w * base_sq.j + base_2.j * norm_accel.x + base_4.w * base_sq.i - base_2.i * norm_accel.y;
		auto s1 = base_4.i * base_sq.k - base_2.k * norm_accel.x + 4.0f * 
			base_sq.w * base.i - base_2.w * norm_accel.y - base_4.i + basei_8 * base_sq.i + basei_8 * base_sq.j + base_4.i * norm_accel.z;
		auto s2 = 4.0f * base_sq.w * base.j + base_2.w * norm_accel.x + base_4.j * 
			base_sq.k - base_2.k * norm_accel.y - base_4.j + basej_8 * base_sq.i + basej_8 * base_sq.j + base_4.j * norm_accel.z;
		auto s3 = 4.0f * base_sq.i * base.k - base_2.i * norm_accel.x + 4.0f * base_sq.j * base.k - base_2.j * norm_accel.y;
		auto anorm = sk_math::FASTINVSQ(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3);
		s0 *= anorm;
		s1 *= anorm;
		s2 *= anorm;
		s3 *= anorm; 
		
		const float beta = 0.1f; //gyro measurement error
		qdot.w -= beta * s0;
		qdot.i -= beta * s1;
		qdot.j -= beta * s2;
		qdot.k -= beta * s3;
			
		base += qdot * dt;
		base.normalize();
		base.toEulerVector(ypr);
	}

	//ultimate high level wrapper -> filters then resolves and updates each state
	//maybe implement an Enum with different filters?? so the filter choice can be passed in?
	void updateState(){
		


	}







};
