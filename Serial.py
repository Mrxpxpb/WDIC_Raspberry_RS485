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

def init_serial(port):
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

def give_all_adr(tries):
    retries = tries
    error_sent = ERROR.NONE
    error_received = ERROR.NONE
    s = ''
    i = 40
    adresses = []
    remove_all_adresses()

    if tries <= 1:
        print("tries must be greater than 0")
        return 
    while error_received != ERROR.TIMEOUT_ERROR:

        give_adr(i,ARG_1.GIVE.value)
        (s, data, error_sent, error_received) = read_frame(True)
        adresses.append(i)
        if error_received != ERROR.TIMEOUT_ERROR and error_received != ERROR.NONE:
            print(f"Unexpected Error occured during adress assignment: {error_received.name}")
            print(s)
            return
        i+=1
    adresses.pop(-1)
    if adresses == []:
        return None    
    return adresses
def give_adr(adress: int, remove_give):
    if adress < 256 and adress > -1 and adress != None:
        adress = "0x{:02x}".format(adress)
        MSB = adress[2].encode()
        LSB = adress[3].encode() 
        write_frame(adress = 0, controll = CTRL.ADR.value, argument_1 = remove_give, data = [MSB, LSB, 0, 0, 0, 0, 0, 0])
        return "Frame sent"
    else:
        return "Wrong Adress value"
def remove_all_adresses():
    write_frame(adress = ADDR.BROADCAST.value, controll = CTRL.ADR.value,argument_1 = ARG_1.REMOVE.value ,data = [0, 0, 0, 0, 0, 0, 0, 0])
    time.sleep(1)
def set_io(device_adr, number, out: bool, on_off: bool) -> str:
    on_off = int(on_off == True)
    if number == 0:
        if out == 1:
            return write_frame(adress = device_adr, controll = CTRL.IO0.value, argument_1 = ARG_1.SET.value, argument_2 = on_off, data = [0, 0, 0, 0, 0, 0, 0, 0])
        return write_frame(adress = 0, controll = CTRL.IO0.value, argument_1 = ARG_1.READ.value, argument_2 = on_off, data = [0, 0, 0, 0, 0, 0, 0, 0])
        
    elif number == 1:
        if out == 1:
            return write_frame(adress = device_adr, controll = CTRL.IO1.value, argument_1 = ARG_1.SET.value, argument_2 = on_off, data = [0, 0, 0, 0, 0, 0, 0, 0])
        return write_frame(adress = 0, controll = CTRL.IO1.value, argument_1 = ARG_1.READ.value, argument_2 = on_off, data = [0, 0, 0, 0, 0, 0, 0, 0])