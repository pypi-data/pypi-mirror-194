# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: t2iapi/operation/service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from t2iapi import basic_responses_pb2 as t2iapi_dot_basic__responses__pb2
from t2iapi.operation import operation_requests_pb2 as t2iapi_dot_operation_dot_operation__requests__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1et2iapi/operation/service.proto\x12\x10t2iapi.operation\x1a\x1ct2iapi/basic_responses.proto\x1a)t2iapi/operation/operation_requests.proto2h\n\x10OperationService\x12T\n\x10SetOperatingMode\x12).t2iapi.operation.SetOperatingModeRequest\x1a\x15.t2iapi.BasicResponseB;\n$com.draeger.medical.t2iapi.operationB\x13OperationApiServiceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 't2iapi.operation.service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n$com.draeger.medical.t2iapi.operationB\023OperationApiService'
  _OPERATIONSERVICE._serialized_start=125
  _OPERATIONSERVICE._serialized_end=229
# @@protoc_insertion_point(module_scope)
