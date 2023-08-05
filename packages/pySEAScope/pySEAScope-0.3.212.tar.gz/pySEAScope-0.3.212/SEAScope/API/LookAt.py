# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class LookAt(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsLookAt(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = LookAt()
        x.Init(buf, n + offset)
        return x

    # LookAt
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # LookAt
    def Lon(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # LookAt
    def Lat(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def LookAtStart(builder): builder.StartObject(2)
def LookAtAddLon(builder, lon): builder.PrependFloat32Slot(0, lon, 0.0)
def LookAtAddLat(builder, lat): builder.PrependFloat32Slot(1, lat, 0.0)
def LookAtEnd(builder): return builder.EndObject()
