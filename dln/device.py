# Copyright (C) 2017  Eldar Khayrullin <eldar.khayrullin@mail.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
DLN-Series Interface Adapters.
Supported Products: DLN-1, DLN-2, DL-4M, DLN-4S
'''


import struct

from .common import *


class Device:
    def __init__(self, client, handle):
        self._client = client
        self._handle = handle

    def get_handle(self):
        return self._handle

    def get_version(self):
        '''
        Retrieves the DLN device and software version data.
        '''
        ...

    def get_device_sn(self):
        '''
        Retrieves the device serial number.
        '''
        ...

    def set_device_id(self, id):
        '''
        Sets a new ID number to the DLN device.
        id: an ID number to be set.
        '''
        ...

    def get_device_id(self):
        '''
        Retrieves the device ID number.
        '''
        ...

    def get_hardware_type(self):
        ...

    def get_hardware_version(self):
        ...

    def get_firmware_version(self):
        ...

    def get_server_version(self):
        cmd = build_msg_header(StructBasicCmd.size, MSG_ID_GET_SERVER_VERSION,
                               0, self._handle)

        sdata = struct.Struct('<I')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def get_library_version(self):
        ...

    def get_pin_cfg(self, pin):
        '''
        Retrieves current configuration of the specified DLN device pin.
        pin: a pin to get the configuration from.
        Return: a current pin configuration.
        Result.SUCCESS - the pin configuration is successfully retrieved.
        Result.INVALID_PIN_NUMBER - an invalid pin number has been specified.
        '''
        ...

    def get_command_restriction(self, msgId, entity):
        ...

    def delay(self, delay):
        ...

    def restart(self):
        ...
