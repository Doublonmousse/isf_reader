# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class IsfFormat(KaitaiStruct):
    """tentative to read the whole of the isf format using ksy."""

    class GuidEnum(IntEnum):
        transform_quad = 72

    class TagTable(IntEnum):
        tag_ink_space_rect = 0
        tag_guid_table = 1
        tag_draw_attrs_table = 2
        tag_draw_attrs_block = 3
        tag_stroke_desc_block = 5
        tag_buttons = 6
        tag_didx = 9
        tag_stroke = 10
        tag_transform_and_scale = 21
        tag_metric_block = 25
        tag_himetric_size = 29
    def __init__(self, _io, _parent=None, _root=None):
        super(IsfFormat, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.hdr = IsfFormat.Header(self._io, self, self._root)
        self.stream_size = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
        self.isf_tag = []
        i = 0
        while not self._io.is_eof():
            self.isf_tag.append(IsfFormat.TableElement(self._io, self, self._root))
            i += 1



    def _fetch_instances(self):
        pass
        self.hdr._fetch_instances()
        self.stream_size._fetch_instances()
        for i in range(len(self.isf_tag)):
            pass
            self.isf_tag[i]._fetch_instances()


    class Bitread(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.Bitread, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.byte = self._io.read_u1()


        def _fetch_instances(self):
            pass

        @property
        def u1(self):
            if hasattr(self, '_m_u1'):
                return self._m_u1

            self._m_u1 = self.byte & 128 > 0
            return getattr(self, '_m_u1', None)

        @property
        def u2(self):
            if hasattr(self, '_m_u2'):
                return self._m_u2

            self._m_u2 = self.byte & 64 > 0
            return getattr(self, '_m_u2', None)

        @property
        def u3(self):
            if hasattr(self, '_m_u3'):
                return self._m_u3

            self._m_u3 = self.byte & 32 > 0
            return getattr(self, '_m_u3', None)

        @property
        def u4(self):
            if hasattr(self, '_m_u4'):
                return self._m_u4

            self._m_u4 = self.byte & 16 > 0
            return getattr(self, '_m_u4', None)

        @property
        def u5(self):
            if hasattr(self, '_m_u5'):
                return self._m_u5

            self._m_u5 = self.byte & 8 > 0
            return getattr(self, '_m_u5', None)

        @property
        def u6(self):
            if hasattr(self, '_m_u6'):
                return self._m_u6

            self._m_u6 = self.byte & 4 > 0
            return getattr(self, '_m_u6', None)

        @property
        def u7(self):
            if hasattr(self, '_m_u7'):
                return self._m_u7

            self._m_u7 = self.byte & 2 > 0
            return getattr(self, '_m_u7', None)

        @property
        def u8(self):
            if hasattr(self, '_m_u8'):
                return self._m_u8

            self._m_u8 = self.byte & 1 > 0
            return getattr(self, '_m_u8', None)


    class BitreadCompression(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.BitreadCompression, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.byte = self._io.read_u1()


        def _fetch_instances(self):
            pass

        @property
        def compression_type(self):
            if hasattr(self, '_m_compression_type'):
                return self._m_compression_type

            self._m_compression_type = self.byte & 192
            return getattr(self, '_m_compression_type', None)

        @property
        def index(self):
            if hasattr(self, '_m_index'):
                return self._m_index

            self._m_index = self.byte & 31
            return getattr(self, '_m_index', None)


    class Buttons(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.Buttons, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.nof_buttons = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.nof_buttons._fetch_instances()


    class CustomGuid(KaitaiStruct):
        """To affine to really take into account all guids Here we suppose the isf_tag == 105 .."""
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.CustomGuid, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tag = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.info = []
            for i in range(4):
                self.info.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.tag._fetch_instances()
            for i in range(len(self.info)):
                pass



    class DaPenTip(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.DaPenTip, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.pen_tip_type = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class DescriptorBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.DescriptorBlock, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tag = self._io.read_u1()
            _on = self.tag
            if _on == 56:
                pass
                self.content = IsfFormat.Buttons(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            _on = self.tag
            if _on == 56:
                pass
                self.content._fetch_instances()


    class Didx(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.Didx, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.value = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.value._fetch_instances()


    class DrawAttribute(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.DrawAttribute, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.size = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.drawing_properties = IsfFormat.DrawingProperties(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.size._fetch_instances()
            self.drawing_properties._fetch_instances()


    class DrawingFlags(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.DrawingFlags, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.drawing_flag = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.drawing_flag._fetch_instances()


    class DrawingProperties(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.DrawingProperties, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tag = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            _on = self.tag.value
            if _on == 72:
                pass
                self.drawing_attribute = IsfFormat.DrawingFlags(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.tag._fetch_instances()
            _on = self.tag.value
            if _on == 72:
                pass
                self.drawing_attribute._fetch_instances()


    class GuidEl(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.GuidEl, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tag = self._io.read_u4be()
            self.b1 = self._io.read_u2be()
            self.b2 = self._io.read_u2be()
            self.ch_list = []
            for i in range(8):
                self.ch_list.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            for i in range(len(self.ch_list)):
                pass



    class GuidTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.GuidTable, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.header = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.guids = []
            for i in range(self.header.value // 16):
                self.guids.append(IsfFormat.GuidEl(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            self.header._fetch_instances()
            for i in range(len(self.guids)):
                pass
                self.guids[i]._fetch_instances()



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.isf_version = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class HimetricSize(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.HimetricSize, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.header = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.himetric_size_x = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.himetric_size_y = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.header._fetch_instances()
            self.himetric_size_x._fetch_instances()
            self.himetric_size_y._fetch_instances()


    class Huffman(KaitaiStruct):
        def __init__(self, n_bytes, codec, _io, _parent=None, _root=None):
            super(IsfFormat.Huffman, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.n_bytes = n_bytes
            self.codec = codec
            self._read()

        def _read(self):
            self.unread = []
            for i in range(self.n_bytes):
                self.unread.append(IsfFormat.BitreadCompression(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.unread)):
                pass
                self.unread[i]._fetch_instances()


        @property
        def codec_f(self):
            """This is the index to point to in the huffman precalculated tables."""
            if hasattr(self, '_m_codec_f'):
                return self._m_codec_f

            self._m_codec_f = self.codec
            return getattr(self, '_m_codec_f', None)


    class InkSpaceRect(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.InkSpaceRect, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.left_d = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.top_d = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.right_d = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.bottom_d = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.left_d._fetch_instances()
            self.top_d._fetch_instances()
            self.right_d._fetch_instances()
            self.bottom_d._fetch_instances()

        @property
        def bottom(self):
            if hasattr(self, '_m_bottom'):
                return self._m_bottom

            self._m_bottom = self.bottom_d.value_signed
            return getattr(self, '_m_bottom', None)

        @property
        def left(self):
            if hasattr(self, '_m_left'):
                return self._m_left

            self._m_left = self.left_d.value_signed
            return getattr(self, '_m_left', None)

        @property
        def right(self):
            if hasattr(self, '_m_right'):
                return self._m_right

            self._m_right = self.right_d.value_signed
            return getattr(self, '_m_right', None)

        @property
        def top(self):
            if hasattr(self, '_m_top'):
                return self._m_top

            self._m_top = self.top_d.value_signed
            return getattr(self, '_m_top', None)


    class MetricBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.MetricBlock, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.header = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unread = []
            for i in range(self.header.value):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.header._fetch_instances()
            for i in range(len(self.unread)):
                pass



    class MultibyteInt(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.MultibyteInt, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.int_value = []
            i = 0
            while True:
                _ = self._io.read_u1()
                self.int_value.append(_)
                if _ & 128 == 0:
                    break
                i += 1


        def _fetch_instances(self):
            pass
            for i in range(len(self.int_value)):
                pass



    class MultibyteIntDecoded(KaitaiStruct):
        """Extracted from https://github.com/kaitai-io/kaitai_struct_formats/blob/5f37c8178a631ae1d50e044be7af58dced0d0b69/common/vlq_base128_le.ksy#L11
        Not sure I understand everything happenning here but it works !
        At least for now, maybe needs to be read attentively to understand/adapt to our usecase
        """
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.MultibyteIntDecoded, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.groups = []
            i = 0
            while True:
                _ = IsfFormat.MultibyteIntDecoded.Group(i, (self.groups[i - 1].interm_value if i != 0 else 0), ((9223372036854775808 if i == 9 else self.groups[i - 1].multiplier * 128) if i != 0 else 1), self._io, self, self._root)
                self.groups.append(_)
                if (not (_.has_next)):
                    break
                i += 1


        def _fetch_instances(self):
            pass
            for i in range(len(self.groups)):
                pass
                self.groups[i]._fetch_instances()


        class Group(KaitaiStruct):
            """One byte group, clearly divided into 7-bit "value" chunk and 1-bit "continuation" flag.
            """
            def __init__(self, idx, prev_interm_value, multiplier, _io, _parent=None, _root=None):
                super(IsfFormat.MultibyteIntDecoded.Group, self).__init__(_io)
                self._parent = _parent
                self._root = _root
                self.idx = idx
                self.prev_interm_value = prev_interm_value
                self.multiplier = multiplier
                self._read()

            def _read(self):
                self.has_next = self._io.read_bits_int_be(1) != 0
                if not self.has_next == (False if self.idx == 9 else self.has_next):
                    raise kaitaistruct.ValidationNotEqualError((False if self.idx == 9 else self.has_next), self.has_next, self._io, u"/types/multibyte_int_decoded/types/group/seq/0")
                self.value = self._io.read_bits_int_be(7)
                if not self.value <= (1 if self.idx == 9 else 127):
                    raise kaitaistruct.ValidationGreaterThanError((1 if self.idx == 9 else 127), self.value, self._io, u"/types/multibyte_int_decoded/types/group/seq/1")


            def _fetch_instances(self):
                pass

            @property
            def interm_value(self):
                """was previously cast as u8 with a."""
                if hasattr(self, '_m_interm_value'):
                    return self._m_interm_value

                self._m_interm_value = (self.prev_interm_value + self.value * self.multiplier)
                return getattr(self, '_m_interm_value', None)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = len(self.groups)
            return getattr(self, '_m_len', None)

        @property
        def value(self):
            """Resulting unsigned value as normal integer."""
            if hasattr(self, '_m_value'):
                return self._m_value

            self._m_value = self.groups[-1].interm_value
            return getattr(self, '_m_value', None)

        @property
        def value_signed(self):
            if hasattr(self, '_m_value_signed'):
                return self._m_value_signed

            self._m_value_signed = (-(self.value) >> 1 if self.value & 1 > 0 else self.value >> 1)
            return getattr(self, '_m_value_signed', None)


    class MultibyteIntSigned(KaitaiStruct):
        """This is the same as multibyte_int as far as parsing goes But there is some difference in how to read the output value For now we don't decode it with the multibyte_int_decoded instance as this isn't needed."""
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.MultibyteIntSigned, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.int_value = []
            i = 0
            while True:
                _ = self._io.read_u1()
                self.int_value.append(_)
                if _ & 128 == 0:
                    break
                i += 1


        def _fetch_instances(self):
            pass
            for i in range(len(self.int_value)):
                pass



    class SingleMetricElement(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.SingleMetricElement, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tag = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.payload_size = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.min = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.max = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unit = self._io.read_u1()
            self.resolution = self._io.read_f4be()


        def _fetch_instances(self):
            pass
            self.tag._fetch_instances()
            self.payload_size._fetch_instances()
            self.min._fetch_instances()
            self.max._fetch_instances()


    class Stroke(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.Stroke, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.cb_stroke = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.cpoints = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.compression_id = self._io.read_u1()
            _on = self.compression_type
            if _on == 0:
                pass
                self.compressed_data = IsfFormat.Uncompressed((self.cb_stroke.value - self.cpoints.len) - 1, self._io, self, self._root)
            elif _on == 128:
                pass
                self.compressed_data = IsfFormat.Huffman((self.cb_stroke.value - self.cpoints.len) - 1, self.compression_id & 31, self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.cb_stroke._fetch_instances()
            self.cpoints._fetch_instances()
            _on = self.compression_type
            if _on == 0:
                pass
                self.compressed_data._fetch_instances()
            elif _on == 128:
                pass
                self.compressed_data._fetch_instances()

        @property
        def compression_type(self):
            if hasattr(self, '_m_compression_type'):
                return self._m_compression_type

            self._m_compression_type = self.compression_id & 192
            return getattr(self, '_m_compression_type', None)


    class TableElement(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.TableElement, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.isf_tag = KaitaiStream.resolve_enum(IsfFormat.TagTable, self._io.read_u1())
            _on = self.isf_tag
            if _on == IsfFormat.TagTable.tag_buttons:
                pass
                self.content = IsfFormat.UnreadTag(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_didx:
                pass
                self.content = IsfFormat.Didx(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_draw_attrs_block:
                pass
                self.content = IsfFormat.TagDrawAttrsBlock(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_draw_attrs_table:
                pass
                self.content = IsfFormat.TagDrawAttrsTable(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_guid_table:
                pass
                self.content = IsfFormat.GuidTable(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_himetric_size:
                pass
                self.content = IsfFormat.HimetricSize(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_ink_space_rect:
                pass
                self.content = IsfFormat.InkSpaceRect(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_metric_block:
                pass
                self.content = IsfFormat.MetricBlock(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_stroke:
                pass
                self.content = IsfFormat.Stroke(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_stroke_desc_block:
                pass
                self.content = IsfFormat.TagStrokeDescBlock(self._io, self, self._root)
            elif _on == IsfFormat.TagTable.tag_transform_and_scale:
                pass
                self.content = IsfFormat.TransformAndScale(self._io, self, self._root)
            else:
                pass
                self.content = IsfFormat.CustomGuid(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            _on = self.isf_tag
            if _on == IsfFormat.TagTable.tag_buttons:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_didx:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_draw_attrs_block:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_draw_attrs_table:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_guid_table:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_himetric_size:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_ink_space_rect:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_metric_block:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_stroke:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_stroke_desc_block:
                pass
                self.content._fetch_instances()
            elif _on == IsfFormat.TagTable.tag_transform_and_scale:
                pass
                self.content._fetch_instances()
            else:
                pass
                self.content._fetch_instances()


    class TagDrawAttrsBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.TagDrawAttrsBlock, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.header = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unread = []
            for i in range(self.header.value):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.header._fetch_instances()
            for i in range(len(self.unread)):
                pass



    class TagDrawAttrsTable(KaitaiStruct):
        """This is a block that can ONLY be decoded once
        """
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.TagDrawAttrsTable, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.size_total = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unread = []
            for i in range(self.size_total.value):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.size_total._fetch_instances()
            for i in range(len(self.unread)):
                pass



    class TagStrokeDescBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.TagStrokeDescBlock, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.size_total = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unread = []
            for i in range(self.size_total.value):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.size_total._fetch_instances()
            for i in range(len(self.unread)):
                pass



    class TransformAndScale(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.TransformAndScale, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.values = []
            for i in range(4):
                self.values.append(self._io.read_f4le())



        def _fetch_instances(self):
            pass
            for i in range(len(self.values)):
                pass



    class Uncompressed(KaitaiStruct):
        def __init__(self, n_bytes, _io, _parent=None, _root=None):
            super(IsfFormat.Uncompressed, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.n_bytes = n_bytes
            self._read()

        def _read(self):
            self.unread = []
            for i in range(self.n_bytes):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            for i in range(len(self.unread)):
                pass



    class UnreadTag(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(IsfFormat.UnreadTag, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.header = IsfFormat.MultibyteIntDecoded(self._io, self, self._root)
            self.unread = []
            for i in range(self.header.value):
                self.unread.append(self._io.read_u1())



        def _fetch_instances(self):
            pass
            self.header._fetch_instances()
            for i in range(len(self.unread)):
                pass




