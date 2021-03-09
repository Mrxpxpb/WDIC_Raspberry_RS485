import re
import subprocess
from serial.tools import list_ports

def get_vid_pid():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    pvids = []
    for i in df.decode().split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    for device in devices:
        pvids.append(device.get('id'))
    return pvids

def get_port_vidpid(vid_pid):
    vp= vid_pid.split(':')
    pid = vp[-1]
    vid = vp[0]
    devices = list_ports.comports()
    for device in devices:
        if device.vid != None or device.pid != None:
            if format(device.vid,'x') == vid and format(device.pid, 'x') == pid:
                return device.device
                break
    return 0
def get_port_manufacturer(manufacturer):
 devices = list_ports.comports()
 for device in devices:
     if device.manufacturer == manufacturer:
        return device.name
        break 

def show_available_devices() -> dict:
    device_dict = dict()
    devices = list_ports.comports()
    for device in devices:
        #print(f'Port: "{device.name}"\n\tManufacturer: "{device.manufacturer}"\n\tDescription: "{device.description}", \n\tHWID: "{device.hwid}"')
        device_dict[device.name] = [device.manufacturer, device.description, device.hwid]
    return device_dict    
