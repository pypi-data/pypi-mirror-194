# vim: ts=4:sts=4:sw=4
#
# @author: <sylvain.herledan@oceandatalab.com>
# @date: 2016-09-08
#
# This file is part of SEAScope, a 3D visualisation and analysis application
# for satellite, in-situ and numerical model data.
#
# Copyright (C) 2014-2023 OceanDataLab
#
# SEAScope is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# SEAScope is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SEAScope. If not, see <https://www.gnu.org/licenses/>.

"""
This module handles the serialization of the getCurrentDatetime command and the
deserialization of the result sent by SEAScope
"""

import logging
import flatbuffers
import SEAScope.API.OpCode
import SEAScope.API.GetCurrentDatetimeResponse
import SEAScope.API.Command
import SEAScope.types.variable

logger = logging.getLogger(__name__)


def serialize(builder):
    """
    Serialize a getCurrentDatetime command using FlatBuffers.

    Parameters
    ----------
    builder : flatbuffers.builder.Builder
        The FlatBuffers builder instance which serializes data. If this
        parameter is None, then a new builder will be created

    Returns
    -------
    tuple(flatbuffers.builder.Builder, int)
        A tuple which contains two elements:

        - the :obj:`flatbuffers.builder.Builder` instance which has been used
          to serialize data
        - an :obj:`int` which is the address/offset of the serialized object
          in the builder buffer
    """
    if builder is None:
        builder = flatbuffers.Builder(0)

    opcode = SEAScope.API.OpCode.OpCode().getCurrentDatetime
    SEAScope.API.Command.CommandStart(builder)
    SEAScope.API.Command.CommandAddOpcode(builder, opcode)
    cmd = SEAScope.API.Command.CommandEnd(builder)

    return builder, cmd


def deserialize(buf):
    """
    Deserialize the response that SEAScope sends after executing the
    getCurrentDatetime command

    Parameters
    ----------
    buf : bytearray
        The buffer which contains the result of the getCurrentDatetime command
        serialized with FlatBuffers

    Returns
    -------
    int
        Current datetime selected in SEAScope timeline, expressed in seconds
        since 1970-01-01T00:00:00Z
    """
    cls = SEAScope.API.GetCurrentDatetimeResponse.GetCurrentDatetimeResponse
    res = cls.GetRootAsGetCurrentDatetimeResponse(buf, 0)

    return res.Timestamp()
