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


import struct

from . import result

MSG_HEADER_FMT = '<HHHH'
BASIC_RSP_FMT = MSG_HEADER_FMT + 'H'    # header + result
BASIC_CMD_FMT = MSG_HEADER_FMT

StructMsgHeader = struct.Struct(MSG_HEADER_FMT)
StructBasicRsp = struct.Struct(BASIC_RSP_FMT)
StructBasicCmd = struct.Struct(BASIC_CMD_FMT)

HANDLE_ALL_DEVICES = 0
HANDLE_INVALID = 0xFFFF

MODULE_DEVICE = 0xFF
MODULE_GENERIC = 0x00
MODULE_GPIO = 0x01
MODULE_SPI_MASTER = 0x02
MODULE_I2C_MASTER = 0x03
MODULE_LED = 0x04
MODULE_BOOT = 0x05
MODULE_ADC = 0x06
MODULE_PWM = 0x07
MODULE_FREQ = 0x08
MODULE_I2S = 0x09
MODULE_SDIO = 0x0A
MODULE_SPI_SLAVE = 0x0B
MODULE_I2C_SLAVE = 0x0C
MODULE_PLS_CNT = 0x0D
MODULE_UART = 0x0E
MODULE_SPI_SLAVE_SYNC = 0x0F
MODULE_I2C_EEPROM = 0x10
MODULE_SPI_EEPROM = 0x11
MODULE_SPI_FLASH = 0x12
MODULE_I2C_DATAFLASH = 0x13
MODULE_ANALYZER = 0x14

MSG_MODULE_POS = 8

MSG_RESULT_LEN = 2

def build_msg_id(id, module):
    return id | module << MSG_MODULE_POS

MSG_ID_OPEN_DEVICE_EX = build_msg_id(0x00, MODULE_DEVICE)
MSG_ID_REGISTER_NOTIFICATION = build_msg_id(0x00, MODULE_GENERIC)
MSG_ID_UNREGISTER_NOTIFICATION = build_msg_id(0x01, MODULE_GENERIC)
MSG_ID_CONNECT = build_msg_id(0x10, MODULE_GENERIC)
MSG_ID_DISCONNECT = build_msg_id(0x11, MODULE_GENERIC)
MSG_ID_DISCONNECT_ALL = build_msg_id(0x12, MODULE_GENERIC)
MSG_ID_GET_SRV_UUID = build_msg_id(0x13, MODULE_GENERIC)
MSG_ID_CLEANUP = build_msg_id(0x14, MODULE_GENERIC)
MSG_ID_CONNECTION_LOST_EV = build_msg_id(0x1F, MODULE_GENERIC)
MSG_ID_GET_DEVICE_COUNT = build_msg_id(0x20, MODULE_GENERIC)
MSG_ID_OPEN_DEVICE = build_msg_id(0x21, MODULE_GENERIC)
MSG_ID_OPEN_STREAM = build_msg_id(0x22, MODULE_GENERIC)
MSG_ID_CLOSE_HANDLE = build_msg_id(0x23, MODULE_GENERIC)
MSG_ID_CLOSE_ALL_HANDLES = build_msg_id(0x24, MODULE_GENERIC)
MSG_ID_DEVICE_REMOVED_EV = build_msg_id(0x2E, MODULE_GENERIC)
MSG_ID_DEVICE_ADDED_EV = build_msg_id(0x2F, MODULE_GENERIC)
MSG_ID_GET_VER = build_msg_id(0x30, MODULE_GENERIC)
MSG_ID_GET_DEVICE_SN = build_msg_id(0x31, MODULE_GENERIC)
MSG_ID_SET_DEVICE_ID = build_msg_id(0x32, MODULE_GENERIC)
MSG_ID_GET_DEVICE_ID = build_msg_id(0x33, MODULE_GENERIC)
MSG_ID_GET_HARDWARE_TYPE = build_msg_id(0x34, MODULE_GENERIC)
MSG_ID_GET_HARDWARE_VERSION = build_msg_id(0x35, MODULE_GENERIC)
MSG_ID_GET_FIRMWARE_VERSION = build_msg_id(0x36, MODULE_GENERIC)
MSG_ID_GET_SERVER_VERSION = build_msg_id(0x37, MODULE_GENERIC)
MSG_ID_GET_LIBRARY_VERSION = build_msg_id(0x38, MODULE_GENERIC)
MSG_ID_GET_PIN_CFG = build_msg_id(0x40, MODULE_GENERIC)
MSG_ID_GET_COMMAND_RESTRICTION = build_msg_id(0x41, MODULE_GENERIC)
MSG_ID_DELAY = build_msg_id(0x42, MODULE_GENERIC)
MSG_ID_RESTART = build_msg_id(0x43, MODULE_GENERIC)

def build_msg_header(size, msg_id, echo_cnt, handle):
    return StructMsgHeader.pack(size, msg_id, echo_cnt, handle)

def check_response(cmd, rsp):
    (size, msg_id, echo_cnt, handle, res) = StructBasicRsp.unpack_from(rsp)
    #TODO check cmd and rsp field
    if not result.issucceeded(res):
        raise Exception(str(result.Result(res)))
    #TODO check result and generate informative exception
