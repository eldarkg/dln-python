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


#Successful return codes  (DLN_RESULT<0x80)
RES_SUCCESS = 0
RES_SUCCESSFUL_REINIT = 1
RES_PENDING = 2
RES_TRANSFER_CANCELLED = 0x20
RES_VALUE_ROUNDED = 0x21

#Error codes  (DLN_RESULT>0x80)
RES_HARDWARE_NOT_FOUND = 0x81
RES_OUTDATED_DRIVER = 0x82
RES_FAIL = 0x83
RES_MESSAGE_ABSENT = 0x84
RES_BAD_PARAMETER = 0x85
RES_MEMORY_ERROR = 0x86
RES_NOT_INITIALIZED = 0x87
RES_INVALID_COMMAND_SIZE = 0x88
RES_INVALID_RESPONSE_SIZE = 0x89
RES_INVALID_MESSAGE_SIZE = 0x8A
RES_NOTIFICATION_NOT_REGISTERED = 0x8B
#RES_INVALID_STREAM_NUMBER = 0x8C
#Use RES_RESPONSE_TIMEOUT instead of RES_TRANSACTION_TIMEOUT
RES_TRANSACTION_TIMEOUT = 0x8D
RES_OPERATION_TIMEOUT = RES_TRANSACTION_TIMEOUT
RES_RESPONSE_WAIT_TIMEOUT = RES_TRANSACTION_TIMEOUT
RES_DEVICE_REMOVED = 0x8E
RES_INVALID_HANDLE = 0x8F
RES_INVALID_MESSAGE_TYPE = 0x90

'''
RES_COMMAND_NOT_SUPPORTED is returned when current command is
not supported by the DLN-series adapter.
There are 2 possible reasons for RES_COMMAND_NOT_SUPPORTED:
1) This command is not supported by this device type. If you need this
functionality, you have to order another DLN-series adapter.
2) You adapter has old firmware version. To enable this functionality simply
update the device firmware.
'''
RES_NOT_IMPLEMENTED = 0x91
RES_COMMAND_NOT_SUPPORTED = RES_NOT_IMPLEMENTED
RES_TOO_MANY_CONNECTIONS = 0x92
RES_ALREADY_INITIALIZED = 0x93
'''
The specified host exists, but the library can't connect to the DLN server
at this host. This can happen when DLN server is not running or its port differs
from the specified one.
'''
RES_CONNECTION_FAILED = 0x94
'''
The RES_MUST_BE_DISABLED error code is returned when the module is enabled
and application makes the configuration changes that are allowed only while
module is disabled. For example SPI frame size can't be changed after you
enable the SPI port.
If you need to change this configuration settings you have to disable the module first.
'''
RES_MUST_BE_DISABLED = 0x95
RES_INTERNAL_ERROR = 0x96
RES_DEVICE_NUMBER_OUT_OF_RANGE = 0x97
'''The host name is longer that MAX_HOST_LENGTH chars'''
RES_HOST_NAME_TOO_LONG = 0x98
'''
The connection to the same DLN server exists.
If the connection was broken and you want to restore it, close the original connection first.
You can use the DlnDisconnect() function to close the original connection.
Afterwards you can call the DlnConnect() function once again to reestablish the connection.
'''
RES_ALREADY_CONNECTED = 0x99
'''
Is is returned after the attempt of sending message through closed connection.
Also it is possible to get it when using handle, which was created with custom connection and
later this connection was closed (by calling DlnDisconnect() function, by loosing connection with DLN Server or if
DLN Server service was stopped).
'''
RES_CONNECTION_LOST = 0xA0
'''
It is returned by DlnDisconnect() function in case of no connection with specified server,
DlnDisconnectAll() returns this result if there are no any connections,
Also it is returned when you try to open device, if there are no connections with DLN server.
'''
RES_NOT_CONNECTED = 0xA1
RES_MESSAGE_SENDING_FAILED = 0xA2
RES_NO_FREE_STREAM = 0xA3
'''Server connection errors'''
'''The specified host does not exist or it is impossible to determine its IP.'''
RES_HOST_LOOKUP_FAILED = 0xA4
RES_PIN_IN_USE = 0xA5
RES_INVALID_LED_NUMBER = 0xA6
RES_INVALID_LED_STATE = 0xA7
RES_INVALID_PORT_NUMBER = 0xA8
RES_INVALID_EVENT_TYPE = 0xA9
RES_PIN_NOT_CONNECTED_TO_MODULE = 0xAA
RES_INVALID_PIN_NUMBER = 0xAB
RES_INVALID_EVENT_PERIOD = 0xAC
'''
Some commands and configuration settings has bit settings reserved for future.
This bits must be set to zero. If DLN-series adapter founds that any of these bits is
set to 1, it returns the RES_CONFIGURATION_NOT_SUPPORTED error code.
'''
RES_NON_ZERO_RESERVED_BIT = 0xAD
RES_INVALID_BUFFER_SIZE = 0xAE
RES_NO_FREE_DMA_CHANNEL = 0xAF
#RES_SPI_DISABLED = 0xB0
#RES_INVALID_SS_OPERATION = 0xB1
#RES_INVALID_SS_NUMBER = 0xB2
RES_INVALID_PLANE_NUMBER = 0xB3
RES_INVALID_ADDRESS = 0xB4
RES_OVERFLOW = 0xB5
RES_BUSY = 0xB6
RES_DISABLED = 0xB7
RES_SPI_INVALID_FRAME_SIZE = 0xB8
RES_INVALID_CHARACTER_LENGTH = RES_SPI_INVALID_FRAME_SIZE
RES_SPI_MASTER_INVALID_SS_VALUE = 0xB9
RES_SPI_MASTER_INVALID_SS_NUMBER = RES_SPI_MASTER_INVALID_SS_VALUE #obsolete
RES_I2C_MASTER_SENDING_ADDRESS_FAILED = 0xBA
RES_I2C_MASTER_SENDING_DATA_FAILED = 0xBB
RES_I2C_MASTER_INVALID_MEM_ADDRESS_LENGTH = 0xBC
RES_I2C_MASTER_ARBITRATION_LOST = 0xBD
RES_I2C_SLAVE_ADDRESS_NEEDED = 0xBE
RES_INVALID_RESOLUTION = 0xBF
RES_INVALID_CHANNEL_NUMBER = 0xC0
RES_CHANNEL_DISABLED = 0xC1
RES_ALL_CHANNELS_DISABLED = 0xC2
RES_INVALID_FREQUENCY = 0xC3
RES_INVALID_BAUDRATE = RES_INVALID_FREQUENCY
RES_PWM_INVALID_DUTY_CYCLE = 0xC4
RES_INVALID_REPLY_TYPE = 0xC5
RES_INVALID_DELAY_VALUE = 0xC6
RES_INVALID_MODE = 0xC7
RES_INVALID_CPOL = 0xC8
RES_INVALID_CPHA = 0xC9
RES_INVALID_TIMEOUT_VALUE = 0xCA
RES_SPI_SLAVE_SS_IDLE_TIMEOUT = 0xCB
RES_INVALID_PARITY = 0xCC
RES_INVALID_STOPBITS = 0xCD
RES_CONFIGURATION_NOT_SUPPORTED = 0xCE
RES_NO_FREE_TIMER = 0xD0
RES_VERIFICATION_ERROR = 0xD1
RES_SOCKET_INITIALIZATION_FAILED = 0xE0
RES_INSUFFICIENT_RESOURCES = 0xE1
RES_INVALID_VALUE = 0xE2

def issucceeded(result):
    return result < 0x40

def iswarning(result):
    return (result >= 0x20) and (result < 0x40)

def isfailed(result):
    return result >= 0x40
