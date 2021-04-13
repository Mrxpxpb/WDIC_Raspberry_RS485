# WDIC_Raspberry_RS485

## Required Hardware
<object data="images/adress_function.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="images/adress_function.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="images/adress_function.pdf">Download PDF</a>.</p>
    </embed>
</object>


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

## Frame Structure
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

### Master Console Commands
These commands can be used by typing ``help`` in the command line

```
help: Returns this text
led0 (ADDRESS) (ON / OFF): turn LED0 on Device with address (ADRESS) on (ON) or off (OFF).
led1 (ADDRESS) (ON / OFF): turn LED1 on Device with address (ADRESS) on (ON) or off (OFF). 
blink: Blinks all LEDs twice.
exit: Exits the programm.
```
### Zuweisung der Befehlswerte beispielhaft

CTRL: Befehl
ARG1 / ARG2: Zusatzoptionen
DATA[0:8] Datenbytes
![alt text](images/befehlswerte.PNG)

### Ping am Oszilloskop
Oben des Gesendete Packet des Raspberry
Unten die Antwort des Slaves
![alt text](images/ping.PNG)
