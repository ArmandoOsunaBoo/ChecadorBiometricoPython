from fprint import *

fprint.init()
devices = fprint.DiscoveredDevices()

if len(devices) > 0:
    dev = devices[0].open_device()
    print_data = dev.enroll_finger_loop()
    print_data = fprint.PrintData.from_data(print_data.data)
    result = dev.verify_finger_loop(print_data)
    assert result is True
    dev.close()