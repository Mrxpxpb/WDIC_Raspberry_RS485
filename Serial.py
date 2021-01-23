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

   