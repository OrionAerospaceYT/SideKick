#pragma once




//unsure if this is good to have in here but for now we have internal 
namespace internal {
    template<typename T, typename U> T pointDiff(const T &p1, const T &p2, const U step) {
        return T(p1.x + ((p2.x - p1.x) * step), (p1.y + ((p2.y - p1.y) * step)));
    }

}//internal 

namespace sk_math {
#define DEG2RAD 0.01745329251
#define RAD2DEG 57.2957795131
//clamps a value between a minimum and a maximum 
template <typename T> T CLAMP(const T value, const T low, const T high) {
	return value < low ? low : (value > high ? high : value);
}

//returns true if a value is close to another value within some margin 
template <typename T> bool ISCLOSE(const T value, const T target, const T error) {
	return !(value < (target - error)) && (value < (target + error));
}

//returns true if value is positive
template <typename T> bool ISPOS(const T value) {
	return value >= 0 ? true : false;
}

//returns the sign of a value (-1,0,1) 
template <typename T> T SIGN(const T value) {
	return T((T(0) < value) - (value < T(0)));
}


//Linear interpolation between two points
template<typename T> T LERP(const T min, const T max, const T interpolationPoint) {
	return T(min + interpolationPoint * (max - min));
}

//A linear interpolation with a slight bezier to the interp to make it smooth 
//https://gamedevbeginner.com/the-right-way-to-lerp-in-unity-with-examples/
template<typename T> T SMOOTLERP(const T min, const T max, const T interpolationPoint) {
	return  T(min + ((interpolationPoint * interpolationPoint) * (3*2*interpolationPoint))*(max - min));
}

//https://stackoverflow.com/questions/785097/how-do-i-implement-a-b%C3%A9zier-curve-in-c
//A quadratic Bezier between 3 points 
//Takes in two vectors and assumes the first two values are the points
//this function should be wrapped into a a for loop to function continously 
template<typename T, typename U> T QUADBEZIER2D(const T &p1, const T &p2, const T &p3, const U step) {
    auto a1 = internal::pointDiff(p1, p2, step);
    auto a2 = internal::pointDiff(p2, p3, step);
    return internal::pointDiff(a1, a2, step);
}

//finds the earth relative acceleration given the two angles
template <typename T> T EARTHA(const T accel, const T phi, const T theta) {
	return (accel / (sqrt(1.0 - ((sin(theta * T(DEG2RAD)) * sin(theta * T(DEG2RAD))) + (sin(phi * T(DEG2RAD)) * sin(phi * T(DEG2RAD)))))));
}

//https:/www.tutorialspoint.com/fast-inverse-square-root-in-cplusplus/
float FASTINVSQ(float n) {
   const float threehalfs = 1.5f;
   float y = n;
   
   long i = * ( long * ) &y;

   i = 0x5f3759df - ( i >> 1 );
   y = * ( float * ) &i;
   
   y = y * ( threehalfs - ( (n * 0.5F) * y * y ) );
   
   return y;
}



}//namespace SKmath








