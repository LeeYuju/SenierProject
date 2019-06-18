# import serial
#
# ser = serial.Serial("/dev/ttyUSB0",9600)
# print (ser.portstr)
# while 1 :
#   ser.readline()

import serial

port = "/dev/ttyUSB0"
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()

while True:
    str_uart = ""
    if(serialFromArduino.inWaiting() > 0):
        input = serialFromArduino.readline().decode("utf-8")
        print(input)
        str_uart += input
