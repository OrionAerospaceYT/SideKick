#pragma once
#include "common.h"
#include "array.h"


//TODO: LOOK INTO INHERT FROM ARRAY STRUCT

//this is a little too geared towards servos at the moment... will need to do more testing with other actuator types 
//assert that size > 1
template <typename T, size_t Size>
struct ActuatorGroup {
    Array<T,Size> a;
    template <typename ...Args>
    constexpr ActuatorGroup(const Args&... args) : a{args...} {}
    void writeAll(int pos) {
            for (auto i = 0; i < Size; ++i){
                 a.data[i].write(pos);
            }
    }
    //add assert
    void write(int actuator_number, int pos){
	a.data[actuator_number].write(pos);
    }
    void attach(int* pins){
	//assert pins length = array size (i.e each actuator must have pin)
	for(auto i = 0; i < Size; ++i){
		a.data[i].attach(*(pins + i));
	}
    }
    void attach(int p1, int p2){
	a.data[0].attach(p1);
	a.data[1].attach(p2);
    }
    //repeated code probably bad
    void attach(int p1, int p2, int p3){
	a.data[0].attach(p1);
	a.data[1].attach(p2);
	a.data[2].attach(p3);
    }
};
