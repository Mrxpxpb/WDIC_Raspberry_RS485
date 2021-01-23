import serial
import time
import usb
import struct
import enum

vid_pid ="10c4:ea60"
ser = serial.Serial()

class FRAME(enum.Enum):
    START = 2
    STOP = 3
    LF = 10

class ADDR(enum.Enum):
    BROADCAST = 0
    MASTER = 1

class CTRL(enum.Enum):
    NONE = 0
    ADR = 1
    GET_STATE = 7
    GET_FRQ = 18
    GET_L = 4
    IO0 = 5
    IO1 = 6
    PING = 17

class ARG_1(enum.Enum):
    NONE = 0
    REMOVE  = 7
    GIVE = 8
    MEASURE_TIME = 100
    SET_IN_OUT = 10
    READ = 11
    SET = 12

class ARG_2(enum.Enum):
    NONE = 0
    

def init_serial():
    port = usb.get_port(vid_pid)
    if port != 0:
        ser.port = port
        ser.baudrate = 57600
        ser.bytesize = 8
        ser.stopbits = 1
        ser.parity = serial.PARITY_NONE
        ser.timeout = 5
        if ser.is_open !=True:
            ser.open()
        return "starting"
    else:
        return "UART Bridge not found"

def write_frame(adress, controll = CTRL.NONE.value, argument_1 = ARG_1.NONE.value, argument_2 = ARG_2.NONE.value, data = [0] * 8): 
    if ser.is_open:
        if adress < 65536 and adress > -1 and adress != None:
            MSB = (adress >> 8) & 0xff
            LSB = adress & 0xff
            MSB = struct.pack('>B',MSB)            
            LSB = struct.pack('>B',LSB)
            print(LSB)            
        else: 
            return "Wrong Adress value"
    else:
            return "CTRL wrong size"

        if argument_1 < 256 and argument_1 > -1:
            argument_1 = struct.pack('>B',argument_1)
        else:
            return "ARG_1 wrong size"

        if argument_2 < 256 and argument_2 > -1:
            argument_2 = struct.pack('>B',argument_2)
        else:
            return "ARG_2 wrong size"    
   