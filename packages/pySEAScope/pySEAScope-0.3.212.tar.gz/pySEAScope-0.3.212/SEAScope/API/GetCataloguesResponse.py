# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GetCataloguesResponse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGetCataloguesResponse(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GetCataloguesResponse()
        x.Init(buf, n + offset)
        return x

    # GetCataloguesResponse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GetCataloguesResponse
    def Sources(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from SEAScope.API.Source import Source
            obj = Source()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # GetCataloguesResponse
    def SourcesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # GetCataloguesResponse
    def SourcesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # GetCataloguesResponse
    def Collections(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from SEAScope.API.Collection import Collection
            obj = Collection()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # GetCataloguesResponse
    def CollectionsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # GetCataloguesResponse
    def CollectionsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def GetCataloguesResponseStart(builder): builder.StartObject(2)
def GetCataloguesResponseAddSources(builder, sources): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(sources), 0)
def GetCataloguesResponseStartSourcesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def GetCataloguesResponseAddCollections(builder, collections): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(collections), 0)
def GetCataloguesResponseStartCollectionsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def GetCataloguesResponseEnd(builder): return builder.EndObject()
