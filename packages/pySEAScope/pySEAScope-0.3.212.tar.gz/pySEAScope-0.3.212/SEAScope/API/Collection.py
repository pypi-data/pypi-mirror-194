# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Collection(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsCollection(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Collection()
        x.Init(buf, n + offset)
        return x

    # Collection
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Collection
    def Id(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from SEAScope.API.RenderableId import RenderableId
            obj = RenderableId()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Collection
    def MustBeCurrent(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Collection
    def XSeamless(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Collection
    def YSeamless(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Collection
    def NewsAligned(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Collection
    def Label(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Collection
    def Tags(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from SEAScope.API.Tag import Tag
            obj = Tag()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Collection
    def TagsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Collection
    def TagsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        return o == 0

    # Collection
    def Variables(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from SEAScope.API.Variable import Variable
            obj = Variable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Collection
    def VariablesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Collection
    def VariablesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        return o == 0

    # Collection
    def DefaultVariable(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

def CollectionStart(builder): builder.StartObject(9)
def CollectionAddId(builder, id): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(id), 0)
def CollectionAddMustBeCurrent(builder, mustBeCurrent): builder.PrependBoolSlot(1, mustBeCurrent, 0)
def CollectionAddXSeamless(builder, xSeamless): builder.PrependBoolSlot(2, xSeamless, 0)
def CollectionAddYSeamless(builder, ySeamless): builder.PrependBoolSlot(3, ySeamless, 0)
def CollectionAddNewsAligned(builder, newsAligned): builder.PrependBoolSlot(4, newsAligned, 0)
def CollectionAddLabel(builder, label): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(label), 0)
def CollectionAddTags(builder, tags): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(tags), 0)
def CollectionStartTagsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CollectionAddVariables(builder, variables): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(variables), 0)
def CollectionStartVariablesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CollectionAddDefaultVariable(builder, defaultVariable): builder.PrependUint32Slot(8, defaultVariable, 0)
def CollectionEnd(builder): return builder.EndObject()
