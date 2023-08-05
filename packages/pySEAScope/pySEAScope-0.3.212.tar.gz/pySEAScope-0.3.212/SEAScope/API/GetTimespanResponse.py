# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GetTimespanResponse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGetTimespanResponse(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GetTimespanResponse()
        x.Init(buf, n + offset)
        return x

    # GetTimespanResponse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GetTimespanResponse
    def Timespan(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from SEAScope.API.Timespan import Timespan
            obj = Timespan()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def GetTimespanResponseStart(builder): builder.StartObject(1)
def GetTimespanResponseAddTimespan(builder, timespan): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(timespan), 0)
def GetTimespanResponseEnd(builder): return builder.EndObject()
