import serial
import time
import usb
import struct
import enum

vid_pid ="10c4:ea60"
ser = serial.Serial()

RED = '\033[91m'
BOLD = '\033[1m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
GREEN = '\033[92m'
END = '\033[0m'
UNDERLINE = '\033[4m'
buffer = ""

class FRAME(enum.Enum):
    START = 2
    STOP = 3
    LF = 10
class ADDR(enum.Enum):
    BROADCAST = 0
    MASTER = 1

class CTRL(enum.Enum):
    NONE = 0
    ADR = 65
    GET_STATE = 83
    GET_FRQ = 70
    GET_L = 76
    IO0 = 48
    IO1 = 49
    CALIBRATE = 67
    PING = 80

class ARG_1(enum.Enum):
    NONE = 0
    REMOVE  = 82
    GIVE = 71
    SET_IN_OUT = 68
    READ = 66
    SET = 73

class ARG_2(enum.Enum):
    NONE = 0

class ERROR(enum.Enum):
    NONE = 0
    TIMEOUT_ERROR = 1
    STX_ERROR = 2
    STOP_LF_ERROR = 3
    LENGTH_MISMATCH_ERROR = 4

def init_serial():
    if port != 0:
        ser.port = port
        ser.baudrate = 57600
        ser.bytesize = 8
        ser.stopbits = 1
        ser.parity = serial.PARITY_NONE
        ser.timeout = 2
        if ser.is_open !=True:
            ser.open()
        print("starting")
    else:
        print("UART Bridge not found")


def write_frame(adress, controll = CTRL.NONE.value, argument_1 = ARG_1.NONE.value, argument_2 = ARG_2.NONE.value, data = [0] * 8): 
    if ser.is_open:
        safetime = 1e-3
        if adress < 256 and adress >= 0 and adress != None:
            adress = "0x{:02x}".format(adress)
            #print(adress)
            MSB = adress[2].encode()
            LSB = adress[3].encode()   
        else: 
            return "Wrong Adress value"
        if controll < 256 and controll > -1:
            controll = struct.pack('>B',controll)
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
        ser.reset_input_buffer()
        ser.reset_output_buffer()  
        ser.write(struct.pack('>B', FRAME.START.value))
        time.sleep(safetime)
        ser.write(MSB)
        time.sleep(safetime)
        ser.write(LSB)
        time.sleep(safetime)
        ser.write(controll)
        time.sleep(safetime)
        ser.write(argument_1)
        time.sleep(safetime)
        ser.write(argument_2)
        time.sleep(safetime)
        
        for i in range(8):
            if data[i] is None:
                ser.write(struct.pack('>B',0))
                time.sleep(safetime)

            elif type(data[i]) is not int:
                ser.write(data[i])
                time.sleep(safetime)
            else:
                ser.write(struct.pack('>B',data[i]))
                time.sleep(safetime)

        ser.write(struct.pack('>B', FRAME.STOP.value))
        time.sleep(safetime)
        ser.write(struct.pack('>B', FRAME.LF.value))
        time.sleep(safetime)
        return "Frame sent"
    else:
        return "Port not open"