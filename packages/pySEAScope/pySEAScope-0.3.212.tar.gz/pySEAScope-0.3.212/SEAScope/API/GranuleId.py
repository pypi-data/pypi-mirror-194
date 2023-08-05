# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GranuleId(object):
    __slots__ = ['_tab']

    # GranuleId
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GranuleId
    def SourceId(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # GranuleId
    def GranuleId(self): return self._tab.Get(flatbuffers.number_types.Uint64Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))

def CreateGranuleId(builder, sourceId, granuleId):
    builder.Prep(8, 16)
    builder.PrependUint64(granuleId)
    builder.Pad(4)
    builder.PrependUint32(sourceId)
    return builder.Offset()
