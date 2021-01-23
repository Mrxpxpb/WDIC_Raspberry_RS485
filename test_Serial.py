import pytest
from Serial import ser, init_serial, FRAME, ARG_1, ARG_2

def test_init_Serial():
    assert init_serial() == "starting"
    ser.write(1)