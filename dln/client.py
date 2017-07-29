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

from device import Device


DEFAULT_SERVER_PORT = 9656


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
            DLN_RES_INSUFFICIENT_RESOURCES;
            DLN_RES_SOCKET_INITIALIZATION_FAILED.
        '''
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        #TODO send message to connection ?!

    def disconnect(self):
        '''
        Closes the connection to the connected DLN server.
        '''
        self._socket.close()

    #FIXME delete
    def disconnect_all(self):
        '''
        Closes connections to all servers at once.
        \retval DLN_RES_SUCCESS - connections to all servers were successfully closed:
        \retval DLN_RES_NOT_CONNECTED - no connections were present during the command execution.
        '''
        ...

    #FIXME delete
    def cleanup(self):
        '''
        Closes all connections and frees the resources used.
        \retval DLN_RES_SUCCESS
        '''
        ...

    def get_device_count(self, deviceCount):
        '''
        Retrieves the total number of DLN-devices available.
        \param deviceCount - A pointer to an unsigned 32-bit integer. This integer will be filled with the total number of available DLN devices.
        '''
        ...

    def open_device(self, number) -> Device:
        '''
        Opens the specified device corresponding to the specified number.
        number: a number of the device to be opened.
        Return:
            DLN_RES_SUCCESS - The device was successfully opened;
            DLN_RES_NOT_CONNECTED - The library was not connected to any server;
            DLN_RES_MEMORY_ERROR - Not enough memory to process this command;
            DLN_RES_HARDWARE_NOT_FOUND - The number of available devices is less than deviceNumber+1;
            DLN_RES_DEVICE_REMOVED - The device was disconnected while opening.
        '''
        #TODO
        return Device(self, handle)

    def open_device_by_sn(self, sn, deviceHandle):
        '''
        Opens a specified defined by its serial number.
        \param sn - A serial number of the DLN device.
        \param deviceHandle - A pointer to the variable that receives the device handle after the function execution.
        '''
        ...

    def open_device_by_id(self, id, deviceHandle):
        '''
        Opens a specified defined by its ID number.
        \param id - An ID number of the DLN device.
        \param deviceHandle - A pointer to the variable that receives the device handle after the function execution.
        '''
        ...

    def open_device_by_hw_type(self, hwType, deviceHandle):
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
        Sends a synchronous command, waits for a response and returns the response details.
        \param command - a pointer to a variable that contains a command to be sent:
        \param responseBufferSize - the maximum number of bytes to be retrieved.
        '''
        self._socket.sendall(cmd)
        return self._socket.recv(size)

    def get_message(self, handle, size) -> bytearray:
        '''
        Retrieves a message (self, response or event) sent by the device.
        \param handle - a handle to the the DLN device;
        \param messageSize - the maximum number of bytes to be retrieved.
        '''
        #TODO check in queue ?!
        msg = self._socket.recv(size)
        #TODO check handle. If handle not equal move msg to queue ?!
        return msg
