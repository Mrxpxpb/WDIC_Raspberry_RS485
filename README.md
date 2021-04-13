# WDIC_Raspberry_RS485
This project is used to switch on LEDs on multiple slave-devices over a serial connection to a computer. The used protocol can also be adopted to add different functionalities like the transmission of measurement values.
## Required Hardware
The hardware consists of a master-slave structure over a common RS485 Bus. 
![alt text](images/adress_function-1.PNG)


For the master a USB to RS485 converter is needed in order to control the bus. The slave-devices can be anything you want as long as they connected to the bus and can understand
the following frame data. 

## Required Python Modules
This project needs pyserial to be installed.

For Windows
```
pip install pyserial
```

For Linux
```
pip3 install pyserial
``` 
## Serial Config
```python
ser.baudrate = 57600
ser.bytesize = 8
ser.stopbits = 1
ser.parity = serial.PARITY_NONE
ser.timeout = 2
```
## Data Frames
The following frame structures list the individual bytes for each frame from the master and the slave. 
### General Structure
![alt text](images/data_frame_structure.PNG)
### Master Request

| ADR_MSB |      | ADR_LSB |      | CTRL  |     |      |          | ARG_1 |     |      |            | ARG_2 |     |      |        | DATA_0  | DATA_1  | DATA_2 | DATA_3 | DATA_4 | DATA_5 | DATA_6 | DATA_7 |
| :-----: | :--: | :-----: | :--: | :---: | :-: | :--: | :------: | :---: | :-: | :--: | :--------: | :---: | :-: | :--: | :----: | :-----: | :-----: | :----: | :----: | :----: | :----: | :----: | :----: |
|   DEC   | HEX  |   DEC   | HEX  | ASCII | DEC | HEX  | Function | ASCII | DEC | HEX  |    NAME    | ASCII | DEC | HEX  |  NAME  |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    0    | 0x00 |   A   | 65  | 0x41 |   ADR    |   G   | 71  | 0x47 |    GIVE    |       |  0  | 0x00 |   -    | ADR_MSB | ADR_LSB |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    0    | 0x00 |       |     |      |          |   R   | 82  | 0x52 |   REMOVE   |       |  0  | 0x00 |   -    |         |         |        |        |        |        |        |        |
|   var   |      |   var   |      |   0   | 48  | 0x30 |   IO0    |   D   | 68  | 0x44 | SET_IN_OUT |       | var | var  | IN_OUT |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|   var   |      |   var   |      |       |     |      |          |   B   | 66  | 0x42 |    READ    |       |  0  | 0x00 |   -    |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|   var   |      |   var   |      |       |     |      |          |   I   | 73  | 0x49 |    SET     |       | var | var  | ON_OFF |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|   var   |      |   var   |      |   1   | 49  | 0x31 |   IO1    |   D   | 68  | 0x44 | SET_IN_OUT |       | var | var  | IN_OUT |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|   var   |      |   var   |      |       |     |      |          |   B   | 66  | 0x42 |    READ    |       |  0  | 0x00 |   -    |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |
|   var   |      |   var   |      |       |     |      |          |   I   | 73  | 0x49 |    SET     |       |  0  | 0x00 | ON_OFF |    -    |    -    |   -    |   -    |   -    |   -    |   -    |   -    |


### Slave Response

| ADR_MSB |      | ADR_LSB |      | CTRL  |     |      |          | ARG_1 |     |      |            | ARG_2 |     |      |        |  DATA_0  | DATA_1 | DATA_2 | DATA_3 | DATA_4 | DATA_5 | DATA_6 | DATA_7 |
| :-----: | :--: | :-----: | :--: | :---: | :-: | :--: | :------: | :---: | :-: | :--: | :--------: | :---: | :-: | :--: | :----: | :------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
|   DEC   | HEX  |   DEC   | HEX  | ASCII | DEC | HEX  | Function | ASCII | DEC | HEX  |    NAME    | ASCII | DEC | HEX  |  NAME  |    -     |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |   A   | 65  | 0x41 |   ADR    |       | 71  | 0x47 |    GIVE    |       |  1  | 0x01 |   -    |    -     |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |   0   | 48  | 0x30 |   IO0    |       | 68  | 0x44 | SET_IN_OUT |       | var | var  | IN_OUT |  IN_OUT  |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |       |     |      |    0     |       | 66  | 0x42 |    READ    |       |  0  | 0x00 |   -    | READ_IO0 |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |       |     |      |    0     |       | 73  | 0x49 |    SET     |       | var | var  | ON_OFF | READ_IO0 |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |   1   | 49  | 0x31 |   IO1    |       | 68  | 0x44 | SET_IN_OUT |       | var | var  | IN_OUT |  IN_OUT  |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |       |     |      |    0     |       | 66  | 0x42 |    READ    |       |  0  | 0x00 |   -    | READ_IO1 |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
|    0    | 0x00 |    1    | 0x01 |       |     |      |    0     |       | 73  | 0x49 |    SET     |       |  0  | 0x00 | ON_OFF | READ_IO1 |   -    |   -    |   -    |   -    |   -    |   -    |   -    |
### Measured Example
In the following image the response of a slave-device to a IO1 turn off command is shown with RS485 signals and ASCII characters.
![alt text](images/slave_resp_measured_dataframe-1.PNG)
## Select the Serial Converter
First you will be asked to select the proper USB device. All available devices will be listed and labeled with a number.
Enter the corresponding number in the terminal and hit enter.


```
0: COM6
        FTDI
        USB Serial Port (COM6)
        USB VID:PID=0403:6001 SER=A10JV1MDA
        
        Select your device
0-0: 
```
## Master Console Commands
These commands can be used by typing ``help`` in the command line

```
help: Returns this text
led0 (ADDRESS) (ON / OFF): turn LED0 on Device with address (ADRESS) on (ON) or off (OFF).
led1 (ADDRESS) (ON / OFF): turn LED1 on Device with address (ADRESS) on (ON) or off (OFF). 
blink: Blinks all LEDs twice.
exit: Exits the programm.
```
## Example
After selecting the USB converter the programm will start and look up all available devices and give them specific adresses. In this case 
the adresses ``40`` and ``41`` have been dealt.  The following commands turn the first LED of the first device on and off. After this all LEDs of all devices
will flash twice and the programm is exited.
```
COM6
starting
Available Addresses: [40, 41]
>led0 40 ON
>led0 40 OFF 
>blink
>exit 
``` 
