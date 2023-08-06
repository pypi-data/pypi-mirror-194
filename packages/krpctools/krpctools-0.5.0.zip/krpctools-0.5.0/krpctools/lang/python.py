import keyword
# pylint: disable=no-name-in-module
from krpc.schema.KRPC_pb2 import Type
from krpc.types import \
    ValueType, ClassType, EnumerationType, MessageType, \
    TupleType, ListType, SetType, DictionaryType
from .language import Language


class PythonLanguage(Language):

    keywords = keyword.kwlist

    value_map = {
        'null': 'None',
        'true': 'True',
        'false': 'False'
    }

    def parse_type(self, typ):
        if isinstance(typ, ValueType):
            # python3 fix: get type name from protobuf type code
            if typ.protobuf_type.code in (Type.SINT64, Type.UINT64):
                return 'int'
            if typ.protobuf_type.code == Type.BYTES:
                return 'bytes'
            if typ.protobuf_type.code == Type.DOUBLE:
                return 'float'
            return typ.python_type.__name__
        if isinstance(typ, MessageType):
            return 'krpc.schema.KRPC.%s' % typ.python_type.__name__
        if isinstance(typ, (ClassType, EnumerationType)):
            return self.shorten_ref(
                '%s.%s' % (typ.protobuf_type.service,
                           typ.protobuf_type.name))
        if isinstance(typ, ListType):
            return 'list'
        if isinstance(typ, DictionaryType):
            return 'dict'
        if isinstance(typ, SetType):
            return 'set'
        if isinstance(typ, TupleType):
            return 'tuple'
        if typ is None:
            return 'None'
        raise RuntimeError('Unknown type \'%s\'' % str(typ))

    def parse_default_value(self, value, typ):
        if (isinstance(typ, ValueType) and
                typ.protobuf_type.code == Type.STRING):
            return '\'%s\'' % value
        # python2 fix: convert set to string manually
        if isinstance(typ, SetType):
            return '{'+', '.join(self.parse_default_value(x, typ.value_type)
                                 for x in value)+'}'
        return str(value)

    def shorten_ref(self, name):
        name = name.split('.')
        if name[0] == self.module:
            del name[0]
        return '.'.join(name)
