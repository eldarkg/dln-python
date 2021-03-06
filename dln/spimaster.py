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
SPI master
'''


from array import array
import struct

from .common import *


# SPI command list
_MSG_ID_GET_PORT_COUNT = build_msg_id(0x00, MODULE_SPI_MASTER)
# Enable, disable
_MSG_ID_ENABLE = build_msg_id(0x11, MODULE_SPI_MASTER)
_MSG_ID_DISABLE = build_msg_id(0x12, MODULE_SPI_MASTER)
_MSG_ID_IS_ENABLED = build_msg_id(0x13, MODULE_SPI_MASTER)
# CPOL + CPHA
_MSG_ID_SET_MODE = build_msg_id(0x14, MODULE_SPI_MASTER)
_MSG_ID_GET_MODE = build_msg_id(0x15, MODULE_SPI_MASTER)
# Transfer size
_MSG_ID_SET_FRAME_SIZE = build_msg_id(0x16, MODULE_SPI_MASTER)
_MSG_ID_GET_FRAME_SIZE = build_msg_id(0x17, MODULE_SPI_MASTER)
# Frequency
_MSG_ID_SET_FREQUENCY = build_msg_id(0x18, MODULE_SPI_MASTER)
_MSG_ID_GET_FREQUENCY = build_msg_id(0x19, MODULE_SPI_MASTER)
# Transfer
_MSG_ID_READ_WRITE = build_msg_id(0x1A, MODULE_SPI_MASTER)
_MSG_ID_READ = build_msg_id(0x1B, MODULE_SPI_MASTER)
_MSG_ID_WRITE = build_msg_id(0x1C, MODULE_SPI_MASTER)
# Delays
_MSG_ID_SET_DELAY_BETWEEN_SS = build_msg_id(0x20, MODULE_SPI_MASTER)
_MSG_ID_GET_DELAY_BETWEEN_SS = build_msg_id(0x21, MODULE_SPI_MASTER)
_MSG_ID_SET_DELAY_AFTER_SS = build_msg_id(0x22, MODULE_SPI_MASTER)
_MSG_ID_GET_DELAY_AFTER_SS = build_msg_id(0x23, MODULE_SPI_MASTER)
_MSG_ID_SET_DELAY_BETWEEN_FRAMES = build_msg_id(0x24, MODULE_SPI_MASTER)
_MSG_ID_GET_DELAY_BETWEEN_FRAMES = build_msg_id(0x25, MODULE_SPI_MASTER)
# SS control
_MSG_ID_SET_SS = build_msg_id(0x26, MODULE_SPI_MASTER)
_MSG_ID_GET_SS = build_msg_id(0x27, MODULE_SPI_MASTER)
_MSG_ID_RELEASE_SS = build_msg_id(0x28, MODULE_SPI_MASTER)
_MSG_ID_SS_VARIABLE_ENABLE = build_msg_id(0x2B, MODULE_SPI_MASTER)
_MSG_ID_SS_VARIABLE_DISABLE = build_msg_id(0x2C, MODULE_SPI_MASTER)
_MSG_ID_SS_VARIABLE_IS_ENABLED = build_msg_id(0x2D, MODULE_SPI_MASTER)
_MSG_ID_SS_AAT_ENABLE = build_msg_id(0x2E, MODULE_SPI_MASTER)
_MSG_ID_SS_AAT_DISABLE = build_msg_id(0x2F, MODULE_SPI_MASTER)
_MSG_ID_SS_AAT_IS_ENABLED = build_msg_id(0x30, MODULE_SPI_MASTER)
_MSG_ID_SS_BETWEEN_FRAMES_ENABLE = build_msg_id(0x31, MODULE_SPI_MASTER)
_MSG_ID_SS_BETWEEN_FRAMES_DISABLE = build_msg_id(0x32, MODULE_SPI_MASTER)
_MSG_ID_SS_BETWEEN_FRAMES_IS_ENABLED = build_msg_id(0x33, MODULE_SPI_MASTER)
_MSG_ID_SET_CPHA = build_msg_id(0x34, MODULE_SPI_MASTER)
_MSG_ID_GET_CPHA = build_msg_id(0x35, MODULE_SPI_MASTER)
_MSG_ID_SET_CPOL = build_msg_id(0x36, MODULE_SPI_MASTER)
_MSG_ID_GET_CPOL = build_msg_id(0x37, MODULE_SPI_MASTER)
_MSG_ID_SS_MULTI_ENABLE = build_msg_id(0x38, MODULE_SPI_MASTER)
_MSG_ID_SS_MULTI_DISABLE = build_msg_id(0x39, MODULE_SPI_MASTER)
_MSG_ID_SS_MULTI_IS_ENABLED = build_msg_id(0x3A, MODULE_SPI_MASTER)
_MSG_ID_GET_SUPPORTED_MODES = build_msg_id(0x40, MODULE_SPI_MASTER)
_MSG_ID_GET_SUPPORTED_CPHA_VALUES = build_msg_id(0x41, MODULE_SPI_MASTER)
_MSG_ID_GET_SUPPORTED_CPOL_VALUES = build_msg_id(0x42, MODULE_SPI_MASTER)
_MSG_ID_GET_SUPPORTED_FRAME_SIZES = build_msg_id(0x43, MODULE_SPI_MASTER)
_MSG_ID_GET_SS_COUNT = build_msg_id(0x44, MODULE_SPI_MASTER)
_MSG_ID_GET_MIN_FREQUENCY = build_msg_id(0x45, MODULE_SPI_MASTER)
_MSG_ID_GET_MAX_FREQUENCY = build_msg_id(0x46, MODULE_SPI_MASTER)
_MSG_ID_GET_MIN_DELAY_BETWEEN_SS = build_msg_id(0x47, MODULE_SPI_MASTER)
_MSG_ID_GET_MAX_DELAY_BETWEEN_SS = build_msg_id(0x48, MODULE_SPI_MASTER)
_MSG_ID_GET_MIN_DELAY_AFTER_SS = build_msg_id(0x49, MODULE_SPI_MASTER)
_MSG_ID_GET_MAX_DELAY_AFTER_SS = build_msg_id(0x4A, MODULE_SPI_MASTER)
_MSG_ID_GET_MIN_DELAY_BETWEEN_FRAMES = build_msg_id(0x4B, MODULE_SPI_MASTER)
_MSG_ID_GET_MAX_DELAY_BETWEEN_FRAMES = build_msg_id(0x4C, MODULE_SPI_MASTER)


class SpiMaster:
    MAX_TRANSFER_SIZE = 256
    # Enabled
    ENABLED = 1
    DISABLED = 0
    # SPI disable
    CANCEL_TRANSFERS = 0
    WAIT_FOR_TRANSFERS = 1
    # Mode: CPHA
    MODE_CPHA_BIT = (1 << 0)
    MODE_CPHA_0 = (0 << 0)
    MODE_CPHA_1 = (1 << 0)
    # Mode: CPOL
    MODE_CPOL_BIT = (1 << 1)
    MODE_CPOL_0 = (0 << 1)
    MODE_CPOL_1 = (1 << 1)
    # Transfer size
    FRAME_SIZE_8 = 8
    FRAME_SIZE_9 = 9
    FRAME_SIZE_10 = 10
    FRAME_SIZE_11 = 11
    FRAME_SIZE_12 = 12
    FRAME_SIZE_13 = 13
    FRAME_SIZE_14 = 14
    FRAME_SIZE_15 = 15
    FRAME_SIZE_16 = 16
    # SS control
    SS_0 = 0xFE
    SS_1 = 0xFD
    SS_2 = 0xFB
    SS_3 = 0xF7
    SS_DECODE_ENABLED = 1
    SS_DECODE_DISABLED = 0
    SS_VARIABLE_ENABLED = 1
    SS_VARIABLE_DISABLED = 0
    SS_AAT_ENABLED = 1
    SS_AAT_DISABLED = 0
    SS_BETWEEN_FRAMES_ENABLED = 1
    SS_BETWEEN_FRAMES_DISABLED = 0
    # read_write_ex attributes
    ATTR_LEAVE_SS_LOW = (1 << 0)
    ATTR_RELEASE_SS = (0 << 0)

    def __init__(self, client, handle):
        self._client = client
        self._handle = handle

    def get_handle(self):
        return self._handle

    def get_port_count(self):
        '''
        Retrieves the total number of SPI master ports available in your
        DLN-series adapter.
        Return: a port count.
        Result.SUCCESS - the port count has been successfully retrieved.
        '''
        cmd = build_msg_header(StructBasicCmd.size, _MSG_ID_GET_PORT_COUNT,
                               0, self._handle)

        sdata = struct.Struct('<B')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def enable(self, port):
        '''
        Activates corresponding SPI master port on your DLN-series adapter.
        port: the number of an SPI master port to be enabled as master.
        Return: a number of the conflicted pin.
        Result.SUCCESS - the SPI master port has been successfully enabled.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.PIN_IN_USE - the SPI pins are assigned to another module of the
        adapter and cannot be enabled as SPI.
        Result.NO_FREE_DMA_CHANNEL - all DMA channels are assigned to another
        modules of the adapter.
        '''
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_ENABLE, 0, self._handle)
        cmd += sdata.pack(port)

        sdata = struct.Struct('<H')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def disable(self, port, wait_for_transfer_completion):
        '''
        Deactivates corresponding SPI master port on your DLN-Series adapter.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to be disabled as master.
        waitForTransferCompletion - wait for current data transfers to complete or disable instantly.
        Result.SUCCESS - the SPI master port has been successfully disabled.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.TRANSFER_CANCELLED - the pending transfers were cancelled.
        '''
        raise Exception("Not implemented")

    def isenabled(self, port, enabled):
        '''
        Retrieves information whether the specified SPI master port is activated.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        enabled - a pointer A pointer to an unsigned 8-bit integer.
        The integer will be filled with information whether the specified SPI master port is activated after the function execution.
        Result.SUCCESS - the SPI master port state has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_mode(self, port, mode):
        '''
        Sets SPI transmission parameters
        port: the number of an SPI master port to apply configuration to;
        mode: a bit field describing the SPI master mode to be set.
        Return:
        Result.SUCCESS - the SPI master port mode has been successfully set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master is busy transferring.
        '''
        sdata = struct.Struct('<BB')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_MODE, 0, self._handle)
        cmd += sdata.pack(port, mode)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def get_mode(self, port, mode):
        '''
         Retrieves current configuration of the specified SPI master port.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        mode - a pointer to an unsigned 8 bit integer. This integer will be filled with the SPI mode description after the function execution.
        Result.SUCCESS - the SPI master port mode has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_frame_size(self, port, size):
        '''
        Sets the size of a single SPI data frame.
        port: the number of an SPI master port to be configured;
        size: a number of bits to be transferred in a single frame.
        Return:
        Result.SUCCESS - the SPI master port frame size has been successfully
        set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.SPI_INVALID_FRAME_SIZE - the frame size is out of range.
        Result.BUSY - the SPI master is busy transferring.
        '''
        sdata = struct.Struct('<BB')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_FRAME_SIZE, 0, self._handle)
        cmd += sdata.pack(port, size)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def get_frame_size(self, port, size):
        '''
        Retrieves current size setting for SPI data frames.
        port: the number of an SPI master port to retrieve the information from.
        Return: a number of bits to be transferred in a single frame.
        Result.SUCCESS - the SPI master port frame size has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_frequency(self, port, freq):
        '''
        Sets  the clock  frequency  on  the SCLK  line.
        port: the number of an SPI master port to be configured;
        freq: sCLK line frequency value, specified in Hz.
        Return: a frequency approximated as the closest to user-defined lower
        value in Hz.
        Result.SUCCESS - the SPI master port frequency has been successfully
        set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master is busy transferring.
        Result.VALUE_ROUNDED - the frequency value has been approximated as the
        closest supported value.
        '''
        sdata = struct.Struct('<BI')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_FREQUENCY, 0, self._handle)
        cmd += sdata.pack(port, freq)

        sdata = struct.Struct('<I')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def get_frequency(self, port, frequency):
        '''
        Retrieves current setting for SPI clock frequency.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        frequency - a pointer to an unsigned 32-bit integer. This integer will be filled with current SPI clock frequency after the function execution.
        Result.SUCCESS - the SPI master port frequency has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def _check_transfer_size(self, size):
        if SpiMaster.MAX_TRANSFER_SIZE < size:
            raise Exception("Maximum transfer bytes should be {0}".
                             format(SpiMaster.MAX_TRANSFER_SIZE))

    def read_write(self, port, buffer):
        '''
        Sends and receives data via SPI.
        port: the number of an SPI master port.
        size: the size of the message buffer.
        buffer: a data to be transferred from master to slave after the function
        execution.
        Return: a data to be transferred from slave to master after the function
        execution.
        Result.SUCCESS - the SPI master port transaction has been successfully
        performed.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.DISABLED - the SPI master port is disabled.
        '''
        return self.read_write_ex(port, buffer, self.ATTR_RELEASE_SS)

    def read_write_ex(self, port, buffer, attr):
        self._check_transfer_size(len(buffer))

        sdata = struct.Struct('<BHB')
        #TODO check transfer size
        cmd = build_msg_header(StructBasicCmd.size + sdata.size + len(buffer),
                               _MSG_ID_READ_WRITE, 0, self._handle)
        cmd += sdata.pack(port, len(buffer), attr)
        cmd += buffer

        sdata = struct.Struct('<H')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size +
                                       len(buffer))
        check_response(cmd, rsp)
        #TODO read from size field
        return rsp[StructBasicRsp.size + sdata.size:]

    def write(self, port, buffer):
        self.write_ex(port, buffer, self.ATTR_RELEASE_SS)

    def write_ex(self, port, buffer, attr):
        self._check_transfer_size(len(buffer))

        sdata = struct.Struct('<BHB')
        #TODO check transfer size
        cmd = build_msg_header(StructBasicCmd.size + sdata.size + len(buffer),
                               _MSG_ID_WRITE, 0, self._handle)
        cmd += sdata.pack(port, len(buffer), attr)
        cmd += buffer

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def read(self, port, size):
        return self.read_ex(port, size, self.ATTR_RELEASE_SS)

    def read_ex(self, port, size, attr):
        self._check_transfer_size(size)

        sdata = struct.Struct('<BHB')
        #TODO check transfer size
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_READ, 0, self._handle)
        cmd += sdata.pack(port, size, attr)

        sdata = struct.Struct('<H')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size +
                                       size)
        check_response(cmd, rsp)
        #TODO read from size field
        return rsp[StructBasicRsp.size + sdata.size:]

    def _convert_frames_to_bytes(self, frames):
        return bytes(array('H', frames))

    def _convert_bytes_to_frames(self, buffer):
        return struct.unpack('<' + str(len(buffer) // 2) + 'H', buffer)

    def read_write_16(self, port, frames):
        '''
        Sends and receives 2-byte frames via SPI.
        port: the number of an SPI master port;
        frames: a data to be transferred from master to slave after the function
        execution.
        Return: a data to be transferred from slave to master after the function
        execution.
        Result.SUCCESS - the SPI master port transaction has been successfully
        performed.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.DISABLED - the SPI master port is disabled.
        '''
        return self.read_write_ex_16(port, frames, self.ATTR_RELEASE_SS)

    def read_write_ex_16(self, port, frames, attr):
        buf = self._convert_frames_to_bytes(frames)
        buf = self.read_write_ex(port, buf, attr)
        return self._convert_bytes_to_frames(buf)

    def write_16(self, port, frames):
        self.write_ex_16(port, frames, self.ATTR_RELEASE_SS)

    def write_ex_16(self, port, frames, attr):
        buf = self._convert_frames_to_bytes(frames)
        self.write_ex(port, buf, self.ATTR_RELEASE_SS)

    def read_16(self, port, size):
        return self.read_ex_16(port, size, self.ATTR_RELEASE_SS)

    def read_ex_16(self, port, size, attr):
        buf = self.read_ex(port, size, self.ATTR_RELEASE_SS)
        return self._convert_bytes_to_frames(buf)

    def set_delay_between_ss(self, port, delay):
        '''
        Sets a minimum delay between release of an SS line and assertion of
        another SS line.
        port: the number of an SPI master port to be configured;
        delay: the delay value in nanoseconds.
        Return: actual set delay value in nanoseconds.
        Result.SUCCESS - the delay has been successfully set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master is busy transferring.
        Result.VALUE_ROUNDED - the delay value has been approximated as the
        closest supported value.
        '''
        sdata = struct.Struct('<BI')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_DELAY_BETWEEN_SS, 0, self._handle)
        cmd += sdata.pack(port, delay)

        sdata = struct.Struct('<I')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def get_delay_between_ss(self, port, delay):
        '''
        Retrieves  current  setting  for  minimum  delay between release of an SS line and assertion of another SS line.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        delayBetweenSS - a  pointer  to  an  unsigned  32-bit  integer.  The  integer  will  be  filled  with  current  delay  value  in nanoseconds.
        Result.SUCCESS - the delay has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_delay_after_ss(self, port, delay):
        '''
        Sets a delay duration between assertion of an SS line and first data
        frame.
        port: the number of an SPI master port to be configured;
        delay: the delay value in nanoseconds.
        Return: actual set delay value in nanoseconds.
        Result.SUCCESS - the delay has been successfully set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master is busy transferring.
        Result.VALUE_ROUNDED - the delay value has been approximated as the
        closest supported value.
        '''
        sdata = struct.Struct('<BI')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_DELAY_AFTER_SS, 0, self._handle)
        cmd += sdata.pack(port, delay)

        sdata = struct.Struct('<I')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def get_delay_after_ss(self, port, delay):
        '''
        Retrieves current setting for minimum delay between assertion of an SS line and first data frame.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        delayAfterSS - a  pointer  to  an  unsigned  32-bit  integer.  The  integer  will  be  filled  with  current  delay  value  in nanoseconds.
        Result.SUCCESS - the delay has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_delay_between_frames(self, port, delay):
        '''
        Sets a delay between data frames exchanged with a single slave device.
        port: the number of an SPI master port to be configured;
        delay: the delay value in nanoseconds.
        Return: actual set delay value in nanoseconds.
        Result.SUCCESS - the delay has been successfully set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master is busy transferring.
        Result.VALUE_ROUNDED - the delay value has been approximated as the
        closest supported value.
        '''
        sdata = struct.Struct('<BI')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_DELAY_BETWEEN_FRAMES,
                               0, self._handle)
        cmd += sdata.pack(port, delay)

        sdata = struct.Struct('<I')
        rsp = self._client.transaction(cmd, StructBasicRsp.size + sdata.size)
        check_response(cmd, rsp)
        return sdata.unpack_from(rsp, StructBasicRsp.size)[0]

    def get_delay_between_frames(self, port, delay_between_frames):
        '''
        Retrieves current setting for delay between data frames exchanged with a single slave device.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        delayBetweenFrames - a  pointer  to  an  unsigned  32-bit  integer.  The  integer  will  be  filled  with  current  delay  value  in nanoseconds.
        Result.SUCCESS - the delay has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_ss(self, port, ss):
        '''
        Selects a Slave Select (self, SS) line.
        port: the number of an SPI master port to be configured;
        ss: an SS line to be activated.
        Return:
        Result.SUCCESS - the slave select has been successfully set.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master port is busy transferring.
        Result.SPI_MASTER_INVALID_SS_NUMBER - the SS value is out of range.
        '''
        sdata = struct.Struct('<BB')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SET_SS, 0, self._handle)
        cmd += sdata.pack(port, ss)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def get_ss(self, port, ss):
        '''
        Retrieves current Slave Select (self, SS)line.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        ss - a pointer to an unsigned 8-bit integer. This integer will be filled with the number of the currently selected SS line.
        Result.SUCCESS - the slave select has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def release_ss(self, port):
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_RELEASE_SS, 0, self._handle)
        cmd += sdata.pack(port)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def ss_variable_enable(self, port):
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SS_VARIABLE_ENABLE, 0, self._handle)
        cmd += sdata.pack(port)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def ss_variable_disable(self, port):
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SS_VARIABLE_DISABLE, 0, self._handle)
        cmd += sdata.pack(port)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def ss_variable_isenabled(self, port, enabled):
        raise Exception("Not implemented")

    def ss_between_frames_enable(self, port):
        '''
        Enables release of an SS line between data frames exchanged with a
        single slave device.
        port: the number of an SPI master port to be configured.
        Return:
        Result.SUCCESS - the SS between frames has been successfully enabled.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master port is busy transferring.
        '''
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SS_BETWEEN_FRAMES_ENABLE,
                               0, self._handle)
        cmd += sdata.pack(port)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def ss_between_frames_disable(self, port):
        '''
        Disables release of an SS line between data frames exchanged with a
        single slave device.
        port: the number of an SPI master port to be configured.
        Return:
        Result.SUCCESS - the SS between frames has been successfully disabled.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        Result.BUSY - the SPI master port is busy transferring.
        '''
        sdata = struct.Struct('<B')
        cmd = build_msg_header(StructBasicCmd.size + sdata.size,
                               _MSG_ID_SS_BETWEEN_FRAMES_DISABLE,
                               0, self._handle)
        cmd += sdata.pack(port)

        rsp = self._client.transaction(cmd, StructBasicRsp.size)
        check_response(cmd, rsp)

    def ss_between_frames_isenabled(self, port, enabled):
        '''
        Retrieves information whether release of an SS line between data frames exchanged with a slave device is enabled.
        handle - a handle to the DLN-series adapter.
        port - the number of an SPI master port to retrieve the information from.
        enabled - a pointer to an unsigned 8-bit integer. The integer will be filled with information whether release of an SS line between data frames exchanged with a slave device is enabled after the function execution.
        Result.SUCCESS - the SS between frames state has been successfully retrieved.
        Result.INVALID_PORT_NUMBER - the port number is out of range.
        '''
        raise Exception("Not implemented")

    def set_cpha(self, port, cpha):
        raise Exception("Not implemented")

    def get_cpha(self, port, cpha):
        raise Exception("Not implemented")

    def set_cpol(self, port, cpol):
        raise Exception("Not implemented")

    def get_cpol(self, port, cpol):
        raise Exception("Not implemented")

    def get_supported_modes(self, port, values):
        raise Exception("Not implemented")

    def get_supported_cpha_values(self, port, values):
        raise Exception("Not implemented")

    def get_supported_cpol_values(self, port, values):
        raise Exception("Not implemented")

    def get_supported_frame_sizes(self, port, supported_sizes):
        raise Exception("Not implemented")

    def get_ss_count(self, port, count):
        raise Exception("Not implemented")

    def ss_multi_enable(self, port, ss_mask):
        raise Exception("Not implemented")

    def ss_multi_disable(self, port, ss_mask):
        raise Exception("Not implemented")

    def ss_multi_isenabled(self, port, enabled):
        raise Exception("Not implemented")

    def ss_enable(self, port, ss):
        raise Exception("Not implemented")

    def ss_disable(self, port, ss):
        raise Exception("Not implemented")

    def ss_isenabled(self, port, ss, enabled):
        raise Exception("Not implemented")
