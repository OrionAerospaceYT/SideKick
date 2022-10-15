import time
import serial
import random
import threading

# the class for dealing with getting data from
# COM ports for the main backend
class DeviceManager():

    # initialisation of variables
    def __init__(self):
        self.device = None
        self.rawData = ""

        self.terminalData = ""
        self.graphTopData = []
        self.graphBottomData = []

    # this function runs on a thread and only gets the
    # raw input data from the com port as a binary string
    # if the device is connected
    def threadedGetRawData(self, port, baud):
        self.device = serial.Serial(port, baud, timeout=0, rtscts=False)
        while self.device != None:
            rawData = self.device.readline().decode("utf-8")
            if "\n" in rawData:
                self.rawData = rawData

    # parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
    # to graphTopData, graphBottomData which are lists
    # example graph output would be: [[1,2,3,4,5,],[5,4,3,2,1],[2,5,4,1,3]]
    #
    # this data still needs to be processed as it is in string form
    # the processing will go in the main backend
    def decodeGraphData(self):
        rawList = self.rawData.split("g(")

        for data in rawList:
            data = data.split(")")
            if "t(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                validGraphData = data[0].replace(" ", "").split(",")
                self.graphTopData.append(validGraphData[2]) if validGraphData[1] == "1" else self.graphBottomData.append(validGraphData[2])

        return self.graphTopData, self.graphBottomData

    # parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
    # to terminalData which is a string
    # all terminal data from one output is put into a single line
    def decodeTerminalData(self):
        rawList = self.rawData.split("t(")
        self.terminalData = ""

        for data in rawList:
            data = data.split(")")
            if "g(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                self.terminalData += " " + data[0]

        return self.terminalData

    # terminates the while True loop to disconnect the device
    # then sets the variables back to the initial states so
    # that there is no data
    def terminateDevice(self):
        self.__init__()

    # connects the device in order to read the data coming
    # from the SideKick/Teensy/Arduino
    # also stars the thread to get the data from the newly connected
    # device
    def connectDevice(self, port="COM1", baud=115200):
        self.getData = threading.Thread(target=self.threadedGetRawData, args=(port, baud),)
        self.getData.start()

# only runs if this is the file being run
# the unit test will go here
if __name__ == "__main__":


    deviceManager = DeviceManager()

    deviceManager.terminateDevice()

    deviceManager.rawData = "g(name,1,1)t(text)g(name,1,2)t(text)g(name,2,3)t(text)"

    # checks the terminal output
    expected = ' text text text'
    output = deviceManager.decodeTerminalData()

    result = "TEST 1: PASS" if output == expected else f"TEST 1: FAIL - Got ({output}) when expecting ({expected})!"
    print(result)

    # checks grpah output
    expected = (["1", "2"], ["3"])
    output = deviceManager.decodeGraphData()

    result = "TEST 2: PASS" if output == expected else f"TEST 2: FAIL - Got ({output}) when expecting ({expected})!"
    print(result)
