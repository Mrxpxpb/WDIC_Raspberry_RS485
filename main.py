import usb
import Serial
import time, struct
import threading

commands = ['help']
Descriptions = {
        'help': 'Returns this text',
        'led0 (ADDRESS) (ON / OFF)': 'turn LED0 on Device with address (ADRESS) on (ON) or off (OFF). ',
        'led1 (ADDRESS) (ON / OFF)': 'turn LED1 on Device with address (ADRESS) on (ON) or off (OFF). ',
        'blink': 'Blinks all LEDs twice.',
        'exit': 'Exits the programm',
}
device_dict = {}
def main():
    global device_dict
    device_dict = (usb.show_available_devices())
    port = ""
    for i, device in enumerate(device_dict):
        print(f'{i}: {device}')
        list = device_dict[device]
        for info in list:
            print(f'\t'+ str(info))
    
    num = get_port()

    for i, device in enumerate(device_dict):
        if i == num:
            manufacturer = device_dict[device][0]
            port = usb.get_port_manufacturer(manufacturer)
    print(port)
    Serial.init_serial(port)
    Serial.ser.timeout = 0.1

    addresses = Serial.give_all_adr(2)
    print(f'Available Addresses: {addresses}')

    while(True):
        line = input('>')
        words = line.split()
        if words == []:
            pass
        elif len(words) == 1:
            if words[0] == "blink":
                blink(addresses)
            elif words[0] == "exit":
                break
            else:
                help()
        elif len(words) == 2:
            help()
        elif len(words) == 3:
            if words[0] == "led0":
                try:
                    address = int(words[1])
                except:
                    print(f"Falsches Adressformat: {words[1]}")
                on_off = False
                if words[2] == "ON":
                    on_off = True
                    led0(address, on_off)
                elif words[2] == "OFF":
                    on_off = False
                    led0(address, on_off)
                else:
                    print("Use ON / OFF as second argument.")
            elif words[0] == "led1":
                try:
                    address = int(words[1])
                except:
                    print(f"Falsches Adressformat: {words[1]}")
                on_off = False
                if words[2] == "ON":
                    on_off = True
                    led1(address, on_off)
                elif words[2] == "OFF":
                    on_off = False
                    led1(address, on_off)
                else:
                    print("Use ON / OFF as second argument.")
            else:
                help()
        else:
            help()
    blink(addresses)
def help():
    for i in Descriptions:
        print(i +': ' + Descriptions[i])
def get_port() -> int:
    global device_dict
    while True:
        try:
            # do stuff
            print(Serial.GREEN + "\n\tSelect your device" + Serial.END)
            s = input(f'0-{len(device_dict) - 1}: ')
            try:
                i = int(s)
                if i < 0 or i > len(device_dict) - 1:
                    raise Exception(f"Select between 0 and {len(device_dict) - 1}")
                return i
            except:
                raise Exception(f"Select between 0 and {len(device_dict) - 1}")
        except Exception as error:
            print(error)

            continue
        break
    


def blink(addresses):
    if addresses == None:
        print("No Addresses")
        return 
    for i in range(4):
        time.sleep(0.2)
        for address in addresses:
            if i % 2 == 0:
                led0(address, True)
                led1(address, True)
            else:
                led0(address, False)
                led1(address, False)
    
    for address in addresses:
            led0(address,False)
            led1(address,False)


def led0(address, on_off: bool):
    Serial.set_io(address, 0, True, on_off)
    Serial.print_frame_error(True)

def led1(address, on_off: bool):
    Serial.set_io(address, 1, True, on_off)
    Serial.print_frame_error(True)
    
if __name__ == "__main__":
    main()

    