# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: registry.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'registry.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eregistry.proto\"7\n\nMapRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1b\n\x13portmapper_location\x18\x02 \x01(\t\"&\n\x08MapReply\x12\x1a\n\x12number_of_services\x18\x01 \x01(\x05\"\x1c\n\x0cUnmapRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\nUnmapReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\"\x1c\n\x0cQueryRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\")\n\nQueryReply\x12\x1b\n\x13portmapper_location\x18\x01 \x01(\t\"\x11\n\x0f\x46inalizeRequest\"2\n\rFinalizeReply\x12!\n\x19registered_services_count\x18\x01 \x01(\x05\x32\xbe\x01\n\x08Registry\x12&\n\nMapService\x12\x0b.MapRequest\x1a\t.MapReply\"\x00\x12,\n\x0cUnmapService\x12\r.UnmapRequest\x1a\x0b.UnmapReply\"\x00\x12,\n\x0cQueryService\x12\r.QueryRequest\x1a\x0b.QueryReply\"\x00\x12.\n\x08\x46inalize\x12\x10.FinalizeRequest\x1a\x0e.FinalizeReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MAPREQUEST']._serialized_start=18
  _globals['_MAPREQUEST']._serialized_end=73
  _globals['_MAPREPLY']._serialized_start=75
  _globals['_MAPREPLY']._serialized_end=113
  _globals['_UNMAPREQUEST']._serialized_start=115
  _globals['_UNMAPREQUEST']._serialized_end=143
  _globals['_UNMAPREPLY']._serialized_start=145
  _globals['_UNMAPREPLY']._serialized_end=173
  _globals['_QUERYREQUEST']._serialized_start=175
  _globals['_QUERYREQUEST']._serialized_end=203
  _globals['_QUERYREPLY']._serialized_start=205
  _globals['_QUERYREPLY']._serialized_end=246
  _globals['_FINALIZEREQUEST']._serialized_start=248
  _globals['_FINALIZEREQUEST']._serialized_end=265
  _globals['_FINALIZEREPLY']._serialized_start=267
  _globals['_FINALIZEREPLY']._serialized_end=317
  _globals['_REGISTRY']._serialized_start=320
  _globals['_REGISTRY']._serialized_end=510
# @@protoc_insertion_point(module_scope)
