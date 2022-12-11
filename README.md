<p align="center">
<img src=https://i.imgur.com/NduHZHs.png width=300 height=150>
</img>
</p>

[![Pylint](https://github.com/OrionAerospaceYT/SideKick/actions/workflows/pylint.yml/badge.svg)](https://github.com/OrionAerospaceYT/SideKick/actions/workflows/pylint.yml)

Table of Contents 
====================
* [What is SideKick?](#What-is-SideKick)
* [What does it run on?](#Hardware)
* [Getting Started?](#Getting-Started)
* [What is SideKick GUI?](#SideKick-GUI)
* [What is ConsciOS?](https://github.com/OrionAerospaceYT/ConsciOS)
---

# What is SideKick?

An expansion/offshoot of the <a href = https://www.arduino.cc/>Arduino</a> ecosystem geared towards more advanced robotics projects. We got tired of using breadboards and rewriting similar code for various robotics projects, so we started working on SideKick -- An advanced framework and ecosystem designed to make the prototyping process for robotics faster.

Currently this entire ecosystem is ina "pre-alpha"

# Hardware

Custom SideKick Hardware will be availabile soon! Register Interest <a href = 'https://docs.google.com/forms/d/e/1FAIpQLSd36gO5EY-KUUJ7Ppadt0nrD7Khohj1LoGKAEagtOyS_skXQg/viewform?usp=sf_link'>HERE</a>

Currently all <b>Arduino</b>, <b>Teensy</b> boards are supported and most SAMD boards by ConsciOS and the GUI.    


# Getting Started

Video Tutorials coming soon! 

It is recommended to have basic experience with Arduino, C++, or ROS before jumping in, but fresh start tutorials will be available. 

Go to <a href = https://github.com/OrionAerospaceYT/SideKick/releases/>Releases</a> and Download 

# SideKick GUI

This is the official SideKick app, designed to be used with SideKick hardware but may also be used with other hardware!<br/>
The SideKick app is to be used for debugging, uploading and managing projects.<br/>
The SideKick app is designed to be used the SideKick C++ framework.<br/>

## Installation

1) To install the App as an executable for normal use go to <a href = https://github.com/OrionAerospaceYT/SideKick/releases/>Releases</a> and download.<br/>
2) Then unzip the downloaded file.
3) Double click the SideKick Setup.exe
4) Follow the instructions on the setup wizard.
5) If you selected desktop shortcut then you may run the app from your desktop.

## Instructions

If you are not using the executable installation you can run the code as a normal python file.
To run this code, I recommend terminal if you are using the .py files and type:
```
python SideKick.py
```
NOTE: If you do not use the executable you will need to install the dependencies.


To connect your SideKick device go to Select COM and select the COM port your device is connected to.<br/>

To disconnect your SideKick  device disconnect.<br/>

To send messages through serial to your device, enter the text under Terminal and click Send.<br/>

To create a SideKick project, enter the Project Name and click New Projects.<br/>

To select the SideKick project, go to the drop down under Select Board.<br/>

To upload the SideKick project click "Upload", with the device connected.<br/>

To save Terminal data, click Record. The blinking light means data is being recorded.<br/>

To save Graph data, right click on the plot you want to save, go to export and select your save location and format.<br/>

## Features

Two graphs with labels and multiple plots for easy debugging.<br/>

Terminal with colour coded error messages from upload.<br/>

SideKick project creation, compilation and upload. <br/>

Saving graph data as CSV, TSV, Matplotlib and png.<br/>

Supported higher baud rates - up to 1024000.              WARNING: data points will be missed at high baud rates.<br/>

Smooth graphics and data plotting in real time.<br/>

Easy to use C++ macros for SideKick hardware.<br/>

Dark mode for a clean looking app.<br/>

## Directory Structure

The file structure is:
```
|--SideKick             # SideKick GUI directory.
|  |
|  |-- Internals        # DO NOT TOUCH.
|  |  |                 # Files to copy to new project.
|  |  |
|  |  | -- Libraries    # ALL SideKick libraries go here.
|  |  |
|  |  | -- Source       # Reference to files which users see in new projects.
|  |
|  |-- Projects
|  |  |
|  |  | -- Libraries    # A copy of the libraries that users import.
|  |  
|  |-- SavedData        # All saved terminal data goes here.
|  |
|  |---- UI             # DO NOT TOUCH
|  |                    # Reference images
|  |
|  |---- SideKick.py    # The file to be run to use the code - not used for executable.
```
