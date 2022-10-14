import time
import serial
import random
import threading

# the class for dealing with getting data from
# COM ports for the main backend
class DeviceManager():

    # initialisation of variables and threads the
    # get raw data
    def __init__(self):
        self.device = None
        self.rawData = ""

        self.terminalData = []
        self.graphTopData = []
        self.graphBottomData = []

        getData = threading.Thread(target=self.threadedGetRawData, args=(),)
        getData.start()

    # this function runs on a thread and only gets the
    # raw input dat from the com port as a binary string
    # if the device is connected
    def threadedGetRawData(self):
        while True:
            if self.device != None:
                self.rawData = self.device.readline()
                self.rawData = str(self.rawData)
                
    # connects the device in order to read the data coming
    # from the SideKick/Teensy/Arduino
    def connectDevice(self, port="COM1", baud=115200):
        self.device = serial.Serial(port, baud, timeout=0, rtscts=False)

    # parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
    # to terminalData, graphTopData, graphBottomData which are string, list,
    # list respectively.
    # example graph output would be: [[1,2,3,4,5,],[5,4,3,2,1],[2,5,4,1,3]]
    def decodeData(self):

        rawList = self.rawData.split("g(")
        
        for data in rawList:
            data = data.split(")")
            if "t(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                validGraphData = data[0].replace(" ", "").split(",")
                if validGraphData[1] == "1":
                    self.graphTopData.append(validGraphData[2])
                if  validGraphData[1] == "2":
                    self.graphBottomData.append(validGraphData[2])
                
        rawList = self.rawData.split("t(")
        self.terminalData = ""
        
        for data in rawList:
            data = data.split(")")
            if "g(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                self.terminalData += data[0] + " "
            
        return self.graphTopData, self.graphBottomData, self.terminalData

    
# only runs if this is the file being run
# the unit test will go here
if __name__ == "__main__":

    deviceManager = DeviceManager()
    
    deviceManager.rawData = "g(name,1,dataTop)t(text)g(name,1,dataTop)t(text)g(name,2,dataBottom)t(text)"
    if deviceManager.decodeData() == (['dataTop', 'dataTop'], ['dataBottom'], 'text text text '):
        print("TEST 1: PASS")
    else:
        print("TEST 1: FAIL")
        
    
