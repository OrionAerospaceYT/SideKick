#pragma once
#include "common.h"
#include "array.h"



//assert that size > 1
template <typename T,typename R,size_t Size>
struct SensorGroup {
    Array<T,Size> a;
    Array<R,Size> r;
    template <typename ...Args>
    constexpr SensorGroup(const Args&... args) : a{args...} {}
    void init(){
	for(auto i = 0; i < Size; ++i){
		a.data[i].init();
	}
    }

    Array<R,Size> read(){
	for(auto i = 0; i < Size; ++i){
		r.data[i] = a.data[i].read();
	}
	return r;
    }
    

};
