#!/usr/bin/env python3

import client

c = client.Client()
c.connect('localhost', client.DEFAULT_SERVER_PORT)
d = client.Device(c, 0)
print(d.get_server_version())
print(c.get_device_count())
d = c.open_device(0)
