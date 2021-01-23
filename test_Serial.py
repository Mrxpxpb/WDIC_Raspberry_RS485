import pytest
from Serial import ser, init_serial, FRAME, ARG_1, ARG_2
test_adress = 9

def test_init_Serial():
    assert init_serial() == "starting"
    #ser.write(1)
def test_give_adr():
    assert write_frame(adress = ADDR.BROADCAST.value, controll = CTRL.ADR.value,argument_1 = ARG_1.GIVE.value ,data = [0, 9, 0, 0, 0, 0, 0, 0]) == "Frame sent"
    assert ser.readline() == b'\x02\x00\x01\x01\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x03\n'
    
def test_ping():
    assert write_frame(adress = 0, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b'\x02\x00\x01\x11\x00\x00\x00\x00\x00\x09\x11\x00\x00\x01\x03\n'
    assert write_frame(adress = test_adress, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b'\x02\x00\x01\x11\x00\x00\x00\x09\x00\x09\x11\x00\x00\x01\x03\n'
    assert write_frame(adress = 69, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b''