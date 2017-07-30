#!/usr/bin/env python3

from dln import *

c = Client()
c.connect('localhost', DEFAULT_SERVER_PORT)
d = Device(c, 0)
print(d.get_server_version())
print(c.get_device_count())
spim = SpiMaster(c, 0)
print(spim.read_write_16(1, (1, 2, 3)))
print(spim.read_write_ex(1, b'aabbcc', SpiMaster.ATTR_RELEASE_SS))
spim.set_frequency(1, 1000000)
spim.set_frame_size(1, SpiMaster.FRAME_SIZE_16)
spim.set_mode(1, SpiMaster.MODE_CPHA_1 | SpiMaster.MODE_CPOL_1)
print(spim.enable(1))
print(spim.get_port_count())
h = c.open_device(0)
