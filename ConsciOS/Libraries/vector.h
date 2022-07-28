#pragma once

#include "sk_math.h"

template <typename T = float>
struct Vec {
    T x = 0;
    T y = 0;
    T z = 0;
    Vec(T a, T b, T c) : x(a), y(b), z(c) {}
    Vec(T a, T b) : x(a), y(b), z(0) {}
    ~Vec() = default;
    Vec() = default;

   //Arduino Override 
	operator String() const {
		return String(x) + "," + String(y) + "," + String(z);
	}

    //OS stream overload
    //friend std::ostream& operator<<(std::ostream& o, const Vec<T> &v){
//	return o << v.x << ", " << v.y << ", " << v.z << std::endl;
  //  }
    T operator[](int i){
	if(i == 0){
	    return x;
	}else if(i == 1){
	    return y;
	}else if(i == 2){
	    return z;
	}
    }

    T get(int i){
	if(i == 0){
	    return x;
	}else if(i == 1){
	    return y;
	}else if(i == 2){
	    return z;
	}
    }
    //Basic Types
    template <typename S>
    Vec operator* (S f) {
        return Vec(x * f, y * f, z * f);
    }
    template <typename S>
    Vec operator/ (S f) {
        return Vec(x / f, y / f, z / f);
    }
    template <typename S>
    Vec operator+ (S f) {
        return Vec(x + f, y + f, z + f);
    }
    template <typename S>
    Vec operator- (S f) {
        return Vec(x - f, y - f, z - f);
    }   

    template <typename S>
    void operator*= (S f) {
         *this = *(this) * f;
    }
    template <typename S>
    void operator/= (S f) {
         *this = *(this) / f;
    }
    //Vector to Vector operations
    Vec operator- (const Vec &v) {
        return Vec(x - v.x, y - v.y, z - v.z);
    }
    Vec operator+= (const Vec &v) {
        return Vec(x += v.x, y += v.y, z += v.z);
    }
    //element wise division 
    Vec operator / (const Vec &v){
	Vec<T> r;
	r.x = x / v.x;
	r.y = y / v.y;
	r.z = z / v.z;
	return r;
    }
    //Cross product 
    Vec operator* (const Vec &v){
	Vec<T> r;
	r.x = (y * v.z - z * v.y);
	r.y = (z * v.x - x * v.z);
	r.z = (x * v.y - y * v.x);
	return r;
    }
    //Vector to Vector Dot Product
    T dot(const Vec &v){
	return x * v.x + y * v.y + z * v.z;
    }

    T magnitude(){
	return sqrt(x * x + y * y + z * z);	
    }

    void normalize(){
	*this = *this / magnitude();	
    }
    
    void toDegrees() {
        *this = (*this) * T(RAD2DEG);
    }
    
    void toRadians() {
        *this = (*this) * T(DEG2RAD);
    }
    //bool functions 
    template <typename S>
    bool operator <(const S f) {
        return (x < f || y < f || z < f);
    }
    template <typename S>
    bool operator >(const S f) {
        return (x > f || y > f || z > f);
    }
    //BLA Matrix conversions
    template <typename S>
    Vec fromMat(const S &mat){
	assert(mat.Cols == 1, "Matrix must have only 1 column");
	return Vec(mat(0),mat(1),mat(2));
    }
    template <typename S>
    S toMat(const S &mat){
	mat(0) = x;
	mat(1) = y;
	mat(2) = z;
	return mat;
    }

};
