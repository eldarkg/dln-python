#!/usr/bin/env python3

import dln

c = dln.Client()
c.connect('localhost', dln.DEFAULT_SERVER_PORT)
d = dln.Device(c, 0)
print(d.get_server_version())
print(c.get_device_count())
d = c.open_device(0)
