import pytest
from Serial import init_serial, FRAME

def test_init_Serial():
    assert init_serial() == "starting"