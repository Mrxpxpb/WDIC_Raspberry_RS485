import usb
import Serial
import time, struct
import threading

def main():
    port = usb.get_port_manufacturer('FTDI')
    Serial.init_serial(port)
    Serial.ser.timeout = 1

    addresses = Serial.give_all_adr(2)
    print(addresses)
    for i in range(10):
        for address in addresses:
            if i % 2 == 0:
                print(Serial.set_io(address, 0, True, True))
                Serial.print_frame_error(True)
                print(Serial.set_io(address, 1, True, True))
                Serial.print_frame_error(True)
            else:
                print(Serial.set_io(address, 0, True, False))
                Serial.print_frame_error(True)
                print(Serial.set_io(address, 1, True, False))
                Serial.print_frame_error(True)

    
if __name__ == "__main__":
    main()