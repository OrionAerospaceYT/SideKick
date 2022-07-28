#pragma once

#include "sk_math.h"
#include "common.h"

//Conversions Taken From Madgwick Paper
//https://www.researchgate.net/publication/221775760_Estimation_of_IMU_and_MARG_orientation_using_a_gradient_descent_algorithm


template <typename T = float>
struct Quat {
  T w = 1;
  T i = 0;
  T j = 0;
  T k = 0;
  Quat(T w, T i, T j, T k) : w(w), i(i), j(j), k(k) {}
  Quat(const Quat& q) : w(q.w), i(q.i), j(q.j), k(q.k) {}
  Quat() = default;
  ~Quat() = default;

//  friend std::ostream& operator<<(std::ostream& o, const Quat<T>& q){
//    return o << q.w << ", " << q.i << ", " << q.j << ", " << q.k << std::endl;
//  }

  //Arduino override for Serial Print

    operator String() const {
  	return String(w) + "," + String(i) + "," + String(j) + "," + String(k);
    }


  //Basic Types
  template <typename S>
  Quat operator* (S f) {
    return Quat(w * f, i * f, j * f, k * f);
  }
  template <typename S>
  Quat operator/ (S f) {
    return Quat(w / f, i / f, j / f, k / f);
  }
  template <typename S>
  Quat operator+ (S f) {
    return Quat(w + f, i + f, j + f, k + f);
  }
  template <typename S>
  Quat operator- (S f) {
    return Quat(w - f, i - f, j - f, k - f);
  }
  template <typename S>
  void operator*= (S f){
  *this = *this * f;
  }
  template <typename S>
  void operator/= (S f){
  *this = *this / f;
  }
  //Quat to Quat operations
  template <typename S>
  Quat operator* (const Quat<S>& q) {
    Quat<T> r;
    r.w = T(w * q.w - i * q.i - j * q.j - k * q.k);
    r.i = T(w * q.i + i * q.w + j * q.k - k * q.j);
    r.j = T(w * q.j - i * q.k + j * q.w + k * q.i);
    r.k = T(w * q.k + i * q.j - j * q.i + k * q.w);
    return r;
  }

 //Division of quaternion A by quaternion B is nothing more than multiplying A by the multiplicative inverse of B
  template <typename S>
  Quat<T> operator/ (Quat<S>& q) {
    Quat<T> r;
    r.w = T((q.w * w + q.i * i + q.j * j + q.k * k) / q.square());
    r.i = T((q.w * i - q.i * w - q.j * k + q.k * j) / q.square());
    r.j = T((q.w * j + q.i * k - q.j * w - q.k * i) / q.square());
    r.k = T((q.w * k - q.i * j - q.j * i - q.k * w) / q.square());
    return r;
  }
  template <typename S>
  Quat<T> operator+ (const Quat<S>& q) {
    return Quat(w + q.w, i + q.i, j + q.j, k + q.k);
  }
  template <typename S>
  Quat<T> operator- (const Quat<S>& q) {
    return Quat(w - q.w, i - q.i, q - q.j, k - q.k);
  }
  template <typename S>
  Quat<T> operator+= (const Quat<S>& q) {
    return Quat(w += q.w, i += q.i, j += q.j, k += q.k);
  }
  template <typename S>
  Quat<T> operator-= (const Quat<S>& q) {
    return Quat(w -= q.w, i -= q.i, j -= q.j, k -= q.k);
  }

  //BOOL operations
  template <typename S>
  bool operator== (const Quat<S>& q) {
    return w == q.w && i == q.i && j == q.j && k == q.k;
  }
  template <typename S>
  bool operator!= (const Quat<S>& q) {
    return !(w == q.w && i == q.i && j == q.j && k == q.k);
  }


  //Convert to Euler Angles array
  T* toEuler() {
    T ypr[3];
    ypr[0] = atan2(T(2) * (i * j + w * k), w * w + i * i - j * j - k * k);
    ypr[1] = -asin(T(2) * (i * k - w * j));
    ypr[2] = atan2(T(2) * (w * i + j * k), w * w - i * i - j * j + k * k);
  }

  //Convert to Euler Angles vector
  template <typename S>
  S toEulerVector(S &vec) {
    vec.x = atan2(T(2) * i * j - T(2) * w * k, T(2) * w * w + T(2) * i * i - T(1));
    auto check = T(2) * i * k + T(2) * w * j;
    if(abs(check) >= T(1)){
	vec.y = -sk_math::SIGN(check) * PI / T(2);
    }else{
    vec.y = -asin(check);
    }
    vec.z = atan2(T(2) * j * k - T(2) * w * i, T(2) * w * w + T(2) * k * k - T(1));
    return vec;
  }

  //Angular rate must be given in rad/s
  template <typename S>
  Quat<T> fromAngularRate(const S &v) {
       	Quat<T> r(0,v.x,v.y,v.z);
        return (*this * T(0.5)) * r;
    }

  template<typename S>
  Quat<T> fromEuler(S x, S y, S z) {
    Quat<T> q;
    q.w = cos(z * T(0.5)) * cos(y * T(0.5)) * cos(x * T(0.5)) + sin(z * T(0.5)) * sin(y * T(0.5)) * sin(x * T(0.5));
    q.x = sin(z * T(0.5)) * cos(y * T(0.5)) *  cos(x * T(0.5)) - cos(z * T(0.5)) * sin(y * T(0.5)) * sin(x * T(0.5));
    q.y = cos(z * T(0.5)) * sin(y * T(0.5)) * cos(x * T(0.5)) + sin(z * T(0.5)) * cos(y * T(0.5)) * sin(x * T(0.5));
    q.z = cos(z * T(0.5)) * cos(y * T(0.5)) * sin(x * T(0.5)) - sin(z * T(0.5)) * sin(y * T(0.5)) * cos(x * T(0.5));
    return q;
  }

  template<typename S>
  Quat<T> fromEuler(const S &v) {
    Quat<T> q;
    q.w = cos(v.z * T(0.5)) * cos(v.y * T(0.5)) * cos(v.x * T(0.5)) + sin(v.z * T(0.5)) * sin(v.y * T(0.5)) * sin(v.x * T(0.5));
    q.x = sin(v.z * T(0.5)) * cos(v.y * T(0.5)) *  cos(v.x * T(0.5)) - cos(v.z * T(0.5)) * sin(v.y * T(0.5)) * sin(v.x * T(0.5));
    q.y = cos(v.z * T(0.5)) * sin(v.y * T(0.5)) * cos(v.x * T(0.5)) + sin(v.z * T(0.5)) * cos(v.y * T(0.5)) * sin(v.x * T(0.5));
    q.z = cos(v.z * T(0.5)) * cos(v.y * T(0.5)) * sin(v.x * T(0.5)) - sin(v.z * T(0.5)) * sin(v.y * T(0.5)) * cos(v.x * T(0.5));
    return q;
  }
  //BLA Matrix conversions
  template <typename S>
  Quat<T> fromMat(const S &mat){
	  assert(mat.Cols == 1, "Matrix must have only 1 column");
	  return Quat(mat(0),mat(1),mat(2),mat(3));
  }
  template <typename S>
  S toMat(S &mat){
	mat(0) = w;
	mat(1) = i;
	mat(2) = j;
	mat(3) = k;
	return mat;
  }

  T magnitude() {
    return sqrt(w * w + i * i + j * j + k * k);
  }

  T square() {
    return w * w + i * i + j * j + k * k;
  }

  Quat<T> squareElements(){
	return Quat<T>(w * w, i * i, j * j, k * k);
  }

  void normalize() {
    *this = Quat((*this) / magnitude());
  }

};
