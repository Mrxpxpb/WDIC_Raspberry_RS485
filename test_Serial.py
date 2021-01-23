import pytest
from Serial import ser, init_serial, FRAME, ARG_1, ARG_2

def test_init_Serial():
    assert init_serial() == "starting"
    #ser.write(1)

def test_ping():
    assert write_frame(adress = 0, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b'\x02\x00\x01\x11\x00\x00\x00\x00\x00\x09\x11\x00\x00\x01\x03\n'
    assert write_frame(adress = test_adress, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b'\x02\x00\x01\x11\x00\x00\x00\x09\x00\x09\x11\x00\x00\x01\x03\n'
    assert write_frame(adress = 69, controll= CTRL.PING.value) == "Frame sent"
    assert ser.readline() == b''