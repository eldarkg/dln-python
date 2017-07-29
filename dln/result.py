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


from enum import IntEnum


class Result(IntEnum):
    #Successful return codes  (DLN_RESULT<0x80)
    SUCCESS = 0
    SUCCESSFUL_REINIT = 1
    PENDING = 2
    TRANSFER_CANCELLED = 0x20
    VALUE_ROUNDED = 0x21
    #Error codes  (DLN_RESULT>0x80)
    HARDWARE_NOT_FOUND = 0x81
    OUTDATED_DRIVER = 0x82
    FAIL = 0x83
    MESSAGE_ABSENT = 0x84
    BAD_PARAMETER = 0x85
    MEMORY_ERROR = 0x86
    NOT_INITIALIZED = 0x87
    INVALID_COMMAND_SIZE = 0x88
    INVALID_RESPONSE_SIZE = 0x89
    INVALID_MESSAGE_SIZE = 0x8A
    NOTIFICATION_NOT_REGISTERED = 0x8B
    #INVALID_STREAM_NUMBER = 0x8C
    #Use RESPONSE_TIMEOUT instead of TRANSACTION_TIMEOUT
    TRANSACTION_TIMEOUT = 0x8D
    OPERATION_TIMEOUT = TRANSACTION_TIMEOUT
    RESPONSE_WAIT_TIMEOUT = TRANSACTION_TIMEOUT
    DEVICE_REMOVED = 0x8E
    INVALID_HANDLE = 0x8F
    INVALID_MESSAGE_TYPE = 0x90
    '''
    COMMAND_NOT_SUPPORTED is returned when current command is
    not supported by the DLN-series adapter.
    There are 2 possible reasons for COMMAND_NOT_SUPPORTED:
    1) This command is not supported by this device type. If you need this
    functionality, you have to order another DLN-series adapter.
    2) You adapter has old firmware version. To enable this functionality simply
    update the device firmware.
    '''
    NOT_IMPLEMENTED = 0x91
    COMMAND_NOT_SUPPORTED = NOT_IMPLEMENTED
    TOO_MANY_CONNECTIONS = 0x92
    ALREADY_INITIALIZED = 0x93
    '''
    The specified host exists, but the library can't connect to the DLN server
    at this host. This can happen when DLN server is not running or its port differs
    from the specified one.
    '''
    CONNECTION_FAILED = 0x94
    '''
    The MUST_BE_DISABLED error code is returned when the module is enabled
    and application makes the configuration changes that are allowed only while
    module is disabled. For example SPI frame size can't be changed after you
    enable the SPI port.
    If you need to change this configuration settings you have to disable the module first.
    '''
    MUST_BE_DISABLED = 0x95
    INTERNAL_ERROR = 0x96
    DEVICE_NUMBER_OUT_OF_RANGE = 0x97
    '''The host name is longer that MAX_HOST_LENGTH chars'''
    HOST_NAME_TOO_LONG = 0x98
    '''
    The connection to the same DLN server exists.
    If the connection was broken and you want to restore it, close the original connection first.
    You can use the DlnDisconnect() function to close the original connection.
    Afterwards you can call the DlnConnect() function once again to reestablish the connection.
    '''
    ALREADY_CONNECTED = 0x99
    '''
    Is is returned after the attempt of sending message through closed connection.
    Also it is possible to get it when using handle, which was created with custom connection and
    later this connection was closed (by calling DlnDisconnect() function, by loosing connection with DLN Server or if
    DLN Server service was stopped).
    '''
    CONNECTION_LOST = 0xA0
    '''
    It is returned by DlnDisconnect() function in case of no connection with specified server,
    DlnDisconnectAll() returns this result if there are no any connections,
    Also it is returned when you try to open device, if there are no connections with DLN server.
    '''
    NOT_CONNECTED = 0xA1
    MESSAGE_SENDING_FAILED = 0xA2
    NO_FREE_STREAM = 0xA3
    '''Server connection errors'''
    '''The specified host does not exist or it is impossible to determine its IP.'''
    HOST_LOOKUP_FAILED = 0xA4
    PIN_IN_USE = 0xA5
    INVALID_LED_NUMBER = 0xA6
    INVALID_LED_STATE = 0xA7
    INVALID_PORT_NUMBER = 0xA8
    INVALID_EVENT_TYPE = 0xA9
    PIN_NOT_CONNECTED_TO_MODULE = 0xAA
    INVALID_PIN_NUMBER = 0xAB
    INVALID_EVENT_PERIOD = 0xAC
    '''
    Some commands and configuration settings has bit settings reserved for future.
    This bits must be set to zero. If DLN-series adapter founds that any of these bits is
    set to 1, it returns the CONFIGURATION_NOT_SUPPORTED error code.
    '''
    NON_ZERO_RESERVED_BIT = 0xAD
    INVALID_BUFFER_SIZE = 0xAE
    NO_FREE_DMA_CHANNEL = 0xAF
    #SPI_DISABLED = 0xB0
    #INVALID_SS_OPERATION = 0xB1
    #INVALID_SS_NUMBER = 0xB2
    INVALID_PLANE_NUMBER = 0xB3
    INVALID_ADDRESS = 0xB4
    OVERFLOW = 0xB5
    BUSY = 0xB6
    DISABLED = 0xB7
    SPI_INVALID_FRAME_SIZE = 0xB8
    INVALID_CHARACTER_LENGTH = SPI_INVALID_FRAME_SIZE
    SPI_MASTER_INVALID_SS_VALUE = 0xB9
    SPI_MASTER_INVALID_SS_NUMBER = SPI_MASTER_INVALID_SS_VALUE #obsolete
    I2C_MASTER_SENDING_ADDRESS_FAILED = 0xBA
    I2C_MASTER_SENDING_DATA_FAILED = 0xBB
    I2C_MASTER_INVALID_MEM_ADDRESS_LENGTH = 0xBC
    I2C_MASTER_ARBITRATION_LOST = 0xBD
    I2C_SLAVE_ADDRESS_NEEDED = 0xBE
    INVALID_RESOLUTION = 0xBF
    INVALID_CHANNEL_NUMBER = 0xC0
    CHANNEL_DISABLED = 0xC1
    ALL_CHANNELS_DISABLED = 0xC2
    INVALID_FREQUENCY = 0xC3
    INVALID_BAUDRATE = INVALID_FREQUENCY
    PWM_INVALID_DUTY_CYCLE = 0xC4
    INVALID_REPLY_TYPE = 0xC5
    INVALID_DELAY_VALUE = 0xC6
    INVALID_MODE = 0xC7
    INVALID_CPOL = 0xC8
    INVALID_CPHA = 0xC9
    INVALID_TIMEOUT_VALUE = 0xCA
    SPI_SLAVE_SS_IDLE_TIMEOUT = 0xCB
    INVALID_PARITY = 0xCC
    INVALID_STOPBITS = 0xCD
    CONFIGURATION_NOT_SUPPORTED = 0xCE
    NO_FREE_TIMER = 0xD0
    VERIFICATION_ERROR = 0xD1
    SOCKET_INITIALIZATION_FAILED = 0xE0
    INSUFFICIENT_RESOURCES = 0xE1
    INVALID_VALUE = 0xE2


def issucceeded(result):
    return result < 0x40

def iswarning(result):
    return (result >= 0x20) and (result < 0x40)

def isfailed(result):
    return result >= 0x40
