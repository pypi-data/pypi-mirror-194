# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class CollectionId(object):
    __slots__ = ['_tab']

    # CollectionId
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CollectionId
    def SourceId(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # CollectionId
    def CollectionId(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreateCollectionId(builder, sourceId, collectionId):
    builder.Prep(4, 8)
    builder.PrependUint32(collectionId)
    builder.PrependUint32(sourceId)
    return builder.Offset()
