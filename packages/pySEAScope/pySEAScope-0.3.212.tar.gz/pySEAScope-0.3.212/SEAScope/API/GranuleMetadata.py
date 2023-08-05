# automatically generated by the FlatBuffers compiler, do not modify

# namespace: API

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GranuleMetadata(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGranuleMetadata(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GranuleMetadata()
        x.Init(buf, n + offset)
        return x

    # GranuleMetadata
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GranuleMetadata
    def SourceId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def CollectionId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def GranuleId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def DataId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def DataModel(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def Start(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def Stop(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # GranuleMetadata
    def Uris(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from SEAScope.API.IDFDescriptor import IDFDescriptor
            obj = IDFDescriptor()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # GranuleMetadata
    def UrisLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # GranuleMetadata
    def UrisIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        return o == 0

    # GranuleMetadata
    def HasTitle(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasInstitution(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasComment(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasFileId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasProductVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasLatMin(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(30))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasLatMax(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(32))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasLonMin(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(34))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasLonMax(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(36))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasCreatorEmail(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(38))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasStationId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(40))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasPlatform(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(42))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def HasSensor(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(44))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GranuleMetadata
    def Title(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(46))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def Institution(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(48))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def Comment(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(50))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def FileId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(52))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def ProductVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(54))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def LatMin(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(56))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GranuleMetadata
    def LatMax(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(58))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GranuleMetadata
    def LonMin(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(60))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GranuleMetadata
    def LonMax(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(62))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GranuleMetadata
    def CreatorEmail(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(64))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def StationId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(66))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def Platform(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(68))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GranuleMetadata
    def Sensor(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(70))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def GranuleMetadataStart(builder): builder.StartObject(34)
def GranuleMetadataAddSourceId(builder, sourceId): builder.PrependUint32Slot(0, sourceId, 0)
def GranuleMetadataAddCollectionId(builder, collectionId): builder.PrependUint32Slot(1, collectionId, 0)
def GranuleMetadataAddGranuleId(builder, granuleId): builder.PrependUint64Slot(2, granuleId, 0)
def GranuleMetadataAddDataId(builder, dataId): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(dataId), 0)
def GranuleMetadataAddDataModel(builder, dataModel): builder.PrependInt8Slot(4, dataModel, 0)
def GranuleMetadataAddStart(builder, start): builder.PrependUint64Slot(5, start, 0)
def GranuleMetadataAddStop(builder, stop): builder.PrependUint64Slot(6, stop, 0)
def GranuleMetadataAddUris(builder, uris): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(uris), 0)
def GranuleMetadataStartUrisVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def GranuleMetadataAddHasTitle(builder, hasTitle): builder.PrependBoolSlot(8, hasTitle, 0)
def GranuleMetadataAddHasInstitution(builder, hasInstitution): builder.PrependBoolSlot(9, hasInstitution, 0)
def GranuleMetadataAddHasComment(builder, hasComment): builder.PrependBoolSlot(10, hasComment, 0)
def GranuleMetadataAddHasFileId(builder, hasFileId): builder.PrependBoolSlot(11, hasFileId, 0)
def GranuleMetadataAddHasProductVersion(builder, hasProductVersion): builder.PrependBoolSlot(12, hasProductVersion, 0)
def GranuleMetadataAddHasLatMin(builder, hasLatMin): builder.PrependBoolSlot(13, hasLatMin, 0)
def GranuleMetadataAddHasLatMax(builder, hasLatMax): builder.PrependBoolSlot(14, hasLatMax, 0)
def GranuleMetadataAddHasLonMin(builder, hasLonMin): builder.PrependBoolSlot(15, hasLonMin, 0)
def GranuleMetadataAddHasLonMax(builder, hasLonMax): builder.PrependBoolSlot(16, hasLonMax, 0)
def GranuleMetadataAddHasCreatorEmail(builder, hasCreatorEmail): builder.PrependBoolSlot(17, hasCreatorEmail, 0)
def GranuleMetadataAddHasStationId(builder, hasStationId): builder.PrependBoolSlot(18, hasStationId, 0)
def GranuleMetadataAddHasPlatform(builder, hasPlatform): builder.PrependBoolSlot(19, hasPlatform, 0)
def GranuleMetadataAddHasSensor(builder, hasSensor): builder.PrependBoolSlot(20, hasSensor, 0)
def GranuleMetadataAddTitle(builder, title): builder.PrependUOffsetTRelativeSlot(21, flatbuffers.number_types.UOffsetTFlags.py_type(title), 0)
def GranuleMetadataAddInstitution(builder, institution): builder.PrependUOffsetTRelativeSlot(22, flatbuffers.number_types.UOffsetTFlags.py_type(institution), 0)
def GranuleMetadataAddComment(builder, comment): builder.PrependUOffsetTRelativeSlot(23, flatbuffers.number_types.UOffsetTFlags.py_type(comment), 0)
def GranuleMetadataAddFileId(builder, fileId): builder.PrependUOffsetTRelativeSlot(24, flatbuffers.number_types.UOffsetTFlags.py_type(fileId), 0)
def GranuleMetadataAddProductVersion(builder, productVersion): builder.PrependUOffsetTRelativeSlot(25, flatbuffers.number_types.UOffsetTFlags.py_type(productVersion), 0)
def GranuleMetadataAddLatMin(builder, latMin): builder.PrependFloat32Slot(26, latMin, 0.0)
def GranuleMetadataAddLatMax(builder, latMax): builder.PrependFloat32Slot(27, latMax, 0.0)
def GranuleMetadataAddLonMin(builder, lonMin): builder.PrependFloat32Slot(28, lonMin, 0.0)
def GranuleMetadataAddLonMax(builder, lonMax): builder.PrependFloat32Slot(29, lonMax, 0.0)
def GranuleMetadataAddCreatorEmail(builder, creatorEmail): builder.PrependUOffsetTRelativeSlot(30, flatbuffers.number_types.UOffsetTFlags.py_type(creatorEmail), 0)
def GranuleMetadataAddStationId(builder, stationId): builder.PrependUOffsetTRelativeSlot(31, flatbuffers.number_types.UOffsetTFlags.py_type(stationId), 0)
def GranuleMetadataAddPlatform(builder, platform): builder.PrependUOffsetTRelativeSlot(32, flatbuffers.number_types.UOffsetTFlags.py_type(platform), 0)
def GranuleMetadataAddSensor(builder, sensor): builder.PrependUOffsetTRelativeSlot(33, flatbuffers.number_types.UOffsetTFlags.py_type(sensor), 0)
def GranuleMetadataEnd(builder): return builder.EndObject()
