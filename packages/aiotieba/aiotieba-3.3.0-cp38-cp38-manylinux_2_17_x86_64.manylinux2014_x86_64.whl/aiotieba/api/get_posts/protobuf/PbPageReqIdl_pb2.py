"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()


from ..._protobuf import CommonReq_pb2 as CommonReq__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12PbPageReqIdl.proto\x1a\x0f\x43ommonReq.proto\"\x92\x02\n\x0cPbPageReqIdl\x12#\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x15.PbPageReqIdl.DataReq\x1a\xdc\x01\n\x07\x44\x61taReq\x12\x1a\n\x06\x63ommon\x18\x19 \x01(\x0b\x32\n.CommonReq\x12\x0b\n\x03tid\x18\x04 \x01(\x03\x12\x1a\n\x12only_thread_author\x18\x05 \x01(\x05\x12\x0c\n\x04sort\x18\x06 \x01(\x05\x12\x0b\n\x03pid\x18\x07 \x01(\x03\x12\x15\n\rwith_comments\x18\x08 \x01(\x05\x12\x12\n\ncomment_rn\x18\t \x01(\x05\x12\n\n\x02rn\x18\r \x01(\x05\x12\n\n\x02pn\x18\x12 \x01(\x05\x12\x1d\n\x15\x63omment_sort_by_agree\x18J \x01(\x05\x12\x0f\n\x07is_fold\x18N \x01(\x05\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PbPageReqIdl_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS is False:
    DESCRIPTOR._options = None
    _globals['_PBPAGEREQIDL']._serialized_start = 40
    _globals['_PBPAGEREQIDL']._serialized_end = 314
    _globals['_PBPAGEREQIDL_DATAREQ']._serialized_start = 94
    _globals['_PBPAGEREQIDL_DATAREQ']._serialized_end = 314
