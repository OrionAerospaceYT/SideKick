# SideKick
<img src = https://i.imgur.com/AurZtde.png> </img>

Table of Contents 
====================
* [What is SideKick?](#What-is-SideKick?)
* [What does it run on?](#Hardware)
* [Getting Started?](#Getting-Started)
* [What is SideKick GUI?](#SideKick-GUI)
* [What is ConsciOS?](#ConsciOS)
---

# What is SideKick?

An expansion/offshoot of the <a href = https://www.arduino.cc/>Arduino</a> ecosystem geared towards more advanced robotics projects. We got tired of using breadboards and rewriting similar code for various robotics projects, so we started working on SideKick -- An advanced framework and ecosystem designed to make the prototyping process for robotics faster.

Currently this entire ecosystem is ina "pre-alpha"

# Hardware

Custom SideKick Hardware will be availabile for purchase soon! Register Interest <a href = https://docs.google.com/forms/d/e/1FAIpQLSd36gO5EY-KUUJ7Ppadt0nrD7Khohj1LoGKAEagtOyS_skXQg/viewform?usp=sf_link>HERE</a>

Currently all Arduino, Teensy boards are supported and most SAMD boards by ConsciOS and the GUI.    


# SideKick GUI

<img src = https://i.imgur.com/7que6wv.png></img>
This is the official SideKick app, designed to be used with SideKick hardware but may also be used with other hardware!<br/>
The SideKick app is to be used for debugging, uploading and managing projects.<br/>
The SideKick app is designed to be used the SideKick C++ framework.<br/>

## Installation

1) To install the App as an executable for normal use go to *link* and download.<br/>
2) Then double click the SK_Install.exe.
3) The files will go to Documents/SideKick.

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

## Dependencies

The exe is an independent app and does not require any external apps.

However for the python code you will need to:
```
pip install PyQt5
pip install serial
pip install pyqtgraph
```
# ConsciOS