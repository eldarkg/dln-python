# Copyright (C) 2017  Eldar Khayrullin <eldar.khayrullin@mail.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY: without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Client generic interface
'''

#TODO return result generate exceptions

import socket
import struct

from .common import *


DEFAULT_SERVER_PORT = 9656

_DEVICE_FILTER_NUMBER = 1 << 0
_DEVICE_FILTER_HW_TYPE = 1 << 1
_DEVICE_FILTER_SN = 1 << 2
_DEVICE_FILTER_ID = 1 << 3
_DEVICE_FILTER_ALL = (_DEVICE_FILTER_NUMBER | _DEVICE_FILTER_SN |
                      _DEVICE_FILTER_ID | _DEVICE_FILTER_HW_TYPE)


class Client:
    def register_notification(self, handle, notification):
        '''
        Registers notification settings
        \param handle - A handle to the DLN device.
        \param notification - Defines the notification settings.
        '''
        ...

    def unregister_notification(self, handle):
        '''
        Unregisters notification settings.
        \param handle - A handle to the DLN device.
        '''
        ...

    def connect(self, host, port):
        '''
        Establishes the connection to the DLN server.
        host: a server to establish the connection to;
        port: a port number of the DLN server.
        Return:
            Result.INSUFFICIENT_RESOURCES;
            Result.SOCKET_INITIALIZATION_FAILED.
        '''
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        #TODO send message to connection ?!

    def disconnect(self):
        '''
        Closes the connection to the connected DLN server.
        '''
        self._socket.close()

    def disconnect_all(self):
        '''
        Closes connections to all servers at once.
        \retval Result.SUCCESS - connections to all servers were successfully closed:
        \retval Result.NOT_CONNECTED - no connections were present during the command execution.
        '''
        ...

    def cleanup(self):
        '''
        Closes all connections and frees the resources used.
        \retval Result.SUCCESS
        '''
        ...

    def get_device_count(self):
        '''
        Retrieves the total number of DLN-devices available.
        '''
        sdata = struct.Struct('<HIII')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               MSG_ID_GET_DEVICE_COUNT, 0, HANDLE_ALL_DEVICES)
        cmd += sdata.pack(0, 0, 0, 0)

        sdata = struct.Struct('<I')
        rsp = self.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def _open_device_common(self, filter, param):
        sdata = struct.Struct('<HIIII')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               MSG_ID_OPEN_DEVICE, 0, HANDLE_ALL_DEVICES)
        cmd += sdata.pack(filter, param, param, param, param)

        sdata = struct.Struct('<I')
        rsp = self.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def open_device(self, number):
        '''
        Opens the specified device corresponding to the specified number.
        number: a number of the device to be opened.
        Return:
            Result.SUCCESS - The device was successfully opened;
            Result.NOT_CONNECTED - The library was not connected to any server;
            Result.MEMORY_ERROR - Not enough memory to process this command;
            Result.HARDWARE_NOT_FOUND - The number of available devices is less than deviceNumber+1;
            Result.DEVICE_REMOVED - The device was disconnected while opening.
        '''
        return self._open_device_common(_DEVICE_FILTER_NUMBER, number)

    def open_device_by_sn(self, sn):
        '''
        Opens a specified defined by its serial number.
        sn: a serial number of the DLN device.
        '''
        return self._open_device_common(_DEVICE_FILTER_SN, sn)

    def open_device_by_id(self, id):
        '''
        Opens a specified defined by its ID number.
        id: an ID number of the DLN device.
        '''
        return self._open_device_common(_DEVICE_FILTER_ID, id)

    def open_device_by_hw_type(self, hw_type):
        return self._open_device_common(_DEVICE_FILTER_HW_TYPE, hw_type)

    def close_handle(self, handle):
        '''
        Closes the handle to an opened DLN device (self, stream).
        handle: a handle to the DLN device.
        '''
        ...

    def close_all_handles(self):
        '''
        Closes handles to all opened DLN devices and streams.
        '''
        ...

    def send_message(self, msg):
        '''
        Sends a specified message (self, an asynchronous command) to the device.
        msg: bytes array that contains a message to be sent.
        '''
        self._socket.sendall(msg)

    def transaction(self, cmd, size) -> bytearray:
        '''
        Sends a synchronous command, waits for a response and returns the
        response details.
        cmd: a pointer to a variable that contains a command to be sent;
        size: the maximum number of bytes to be retrieved.
        '''
        self._socket.sendall(cmd)
        return self._socket.recv(size)

    def get_message(self, handle, size) -> bytearray:
        '''
        Retrieves a message (self, response or event) sent by the device.
        handle: a handle to the the DLN device;
        size: the maximum number of bytes to be retrieved.
        '''
        #TODO check in queue ?!
        msg = self._socket.recv(size)
        #TODO check handle. If handle not equal move msg to queue ?!
        return msg
