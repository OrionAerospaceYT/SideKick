#pragma once
//-----Internals------
#include "sensor_struct.h"
#include "common.h"
//-----Internals------


//Include your sensor libraries here

#include "MPU6050_tockn.h" // My imu library
#include "Wire.h"

#include "vector.h"
#include "quaternion.h"

namespace sensors{

  MPU6050 imu(Wire1); // my board is running on Wire1 (Teensy4.1) most will use Wire

  Quat<float> base = {1.0f, 0.0f, 0.0f, 0.0f}; // Quaternion base definition
  Quat<float> q_dot;

  void init(){
    Wire1.begin();  // Begins Wire1
    imu.begin(); // Initialises the IMU (MPU6050)
  }

  void update(Vec<float> &ypr_rate, Vec<float> &ypr, float dt){
    // Updates the sensor readings
    imu.update();

    // Sets the ypr_rate reference to the new values
    ypr_rate.x = imu.getGyroX();
    ypr_rate.y = imu.getGyroY();
    ypr_rate.z = imu.getGyroZ();

    // Converts to radians for orientation calculation
    ypr_rate.toRadians();

    // Performs the quaternion calculations
    q_dot = base.fromAngularRate(ypr_rate);
    base = base + q_dot * dt;

    // Converts yaw pitch roll rate to degrees for graphing
    ypr_rate.toDegrees();

    // Converts yaw pitch roll to Euler angles and degrees
    base.toEulerVector(ypr);
    ypr.toDegrees();
  }

}//namespace Sensors
