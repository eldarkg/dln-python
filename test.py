#!/usr/bin/env python3

from dln import *

c = Client()
c.connect('localhost', DEFAULT_SERVER_PORT)
print(c.get_device_count())

h = c.open_device(0)
d = Device(c, h)
print(d.get_server_version())

spim = SpiMaster(c, h)
print(spim.get_port_count())

spim.set_frequency(0, 2000000)
spim.set_frame_size(0, SpiMaster.FRAME_SIZE_16)
spim.set_mode(0, SpiMaster.MODE_CPHA_1 | SpiMaster.MODE_CPOL_1)
spim.ss_between_frames_enable(0)
print(spim.set_delay_between_frames(0, 0))
print(spim.set_delay_after_ss(0, 500))
print(spim.set_delay_between_ss(0, 250))
print(spim.enable(0))
print(spim.read_write_16(0, (1, 2)))
