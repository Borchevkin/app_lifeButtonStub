#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Stub for Life Button App

Features:
    - work with serial port over pyserial module
    - emulate some command chains for Life Button Wrist
    - TBA

Created on Thu Aug  3 16:31:11 2017

@author: Danil Borchevkin
"""

# Config constants
# Port name for linux must be /dev/ttyXXXX. For WIndows - COMx
PORT_NAME = "COM3"
# Port parameters and speed constraint by firmware of the stub. Don't change!
# Port speed is 115200
PORT_SPEED = 115200
# Enabling hardware flow control
PORT_HWFC = 1
# End of config constants

# Life Button protocol

LB_START_BYTE = 0xAB
LB_STATUS_HEART_RATE_SINGLE = 0x09
LB_STATUS_SPO2_SINGLE = 0x11


# End of Life Button protocol


import serial
import logging

def heartRateSignleMeasurementHandler(data):
    """
    For get this answer need to sent AB 05 FF 31 09 00 FF 
    """
    # Only for testing - no detailed parsing, just form answer
    return bytearray([0xAB, 0x04, 0xFF, 0x31, 0x09, 0x44])
    
def spo2SignleMeasurementHandler(data):
    """
    For get this answer need to sent AB 05 FF 31 11 00 FF 
    """
    # Only for testing - no detailed parsing, just form answer
    return bytearray([0xAB, 0x04, 0xFF, 0x31, 0x11, 0x22])
    pass

def parseProtocolData(data):
    # Simple parsing
    # Check only Status byte
    logging.debug("Status byte equals to " + hex(data[2]))
    
    if data[2] == LB_STATUS_HEART_RATE_SINGLE:
        logging.info("Request for heart rate single measurement")
        return heartRateSignleMeasurementHandler(data)
    elif data[2] == LB_STATUS_SPO2_SINGLE:
        logging.info("Request for SPO2 single measurement")
        return spo2SignleMeasurementHandler(data)
    
    # If ID not recognized return 0xFF 0xFF 0xFF 0xFF
    return bytearray([0xFF, 0xFF, 0xFF, 0xFF])

def serialHandler():
    """
    Handler for serial port connection
    """
    incomingData = []
    
    with serial.Serial(PORT_NAME, PORT_SPEED, rtscts=PORT_HWFC) as port:
        while True:
            # Read one byte from serial port
            incomingByte = port.read(size=1)
            
            # Echo to terminal. Used for appears typing text
            #port.write(bytearray(incomingByte))
            
            # Parse incoming byte
            
            # If get start of packet byte - receive next byte with overall len of the packet
            if ord(incomingByte) == LB_START_BYTE:
                logging.debug("Received start byte 0xAB")
                
                # Receife start byte. Next - length byte
                lenByte = port.read(size=1)
                logging.debug("Received length of data = " + str(lenByte))
                
                # Waiting exaclty length byte chain
                incomingData = port.read(size=ord(lenByte))
                logging.debug("Finish receive of the data bytes")
                
                # Parse data and forming a answer
                answer = parseProtocolData(incomingData)
                
                # Write answer to the port
                port.write(answer)
                
                # Flush serial port buffer to send data physically
                port.flush()
            else:
                # This is no a start byte
                # Think about it
                pass
            # End of parse incoming byte
    

if __name__ == "__main__":
    # Config logging module
    logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.DEBUG)
    
    # Welcome message
    logging.info("Stub for Life Button App is launched")
    
    # Run handler
    try:
        serialHandler()
            
    except KeyboardInterrupt:
        print("\nCtrl+C is received. Exit from script...")
    
    # Goodbye message
    logging.info("Exit from Stub for Life Button App")