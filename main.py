import usb
import Serial
import time, struct
import threading

def main():
    port = usb.get_port_manufacturer('FTDI')
    Serial.init_serial(port)
    Serial.give_all_adr(1)
    Serial.ser.timeout = 1

    addresses = Serial.give_all_adr(2)

    for i in range(10):
        for address in addresses:
            if i % 2 == 0:
                Serial.set_io(address, 0, True, True)
                Serial.set_io(address, 1, True, True)
            else:
                Serial.set_io(address, 0, True, False)
                Serial.set_io(address, 1, True, False)    

    
if __name__ == "__main__":
    main()