import pytest
from Serial import init_serial, FRAME, ARG_1, ARG_2

def test_init_Serial():
    assert init_serial() == "starting"