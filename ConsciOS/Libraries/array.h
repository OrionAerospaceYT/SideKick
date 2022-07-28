#pragma once
#include "common.h"



//thanks to Martin Starkov for help with the basics of this struct
//assert that size > 1
template <typename T, size_t Size>
struct Array {
    T data[Size];
    template <typename ...Args>
    constexpr Array(const Args&... args) : data{args...} {}
    constexpr Array() : data{} {}
    T get(int i){
	return data[i];
    }

    operator String(){
	    String ret;
	    for(auto i = 0; i < Size - 1; ++i){
		ret += String(data[i]) + ",";
	    }
	    ret += String(data[Size - 1]);
	    return ret;
    }
    T operator [](int i){
	return data[i];
    }
    

};
