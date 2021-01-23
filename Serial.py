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

   