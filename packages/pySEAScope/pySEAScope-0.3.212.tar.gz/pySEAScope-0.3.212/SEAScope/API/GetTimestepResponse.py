# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GetTimestepResponse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGetTimestepResponse(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GetTimestepResponse()
        x.Init(buf, n + offset)
        return x

    # GetTimestepResponse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GetTimestepResponse
    def Timestep(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from SEAScope.API.Timestep import Timestep
            obj = Timestep()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def GetTimestepResponseStart(builder): builder.StartObject(1)
def GetTimestepResponseAddTimestep(builder, timestep): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(timestep), 0)
def GetTimestepResponseEnd(builder): return builder.EndObject()
