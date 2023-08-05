# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streamlit/proto/Delta.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from streamlit.proto import Block_pb2 as streamlit_dot_proto_dot_Block__pb2
from streamlit.proto import Element_pb2 as streamlit_dot_proto_dot_Element__pb2
from streamlit.proto import NamedDataSet_pb2 as streamlit_dot_proto_dot_NamedDataSet__pb2
from streamlit.proto import ArrowNamedDataSet_pb2 as streamlit_dot_proto_dot_ArrowNamedDataSet__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='streamlit/proto/Delta.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1bstreamlit/proto/Delta.proto\x1a\x1bstreamlit/proto/Block.proto\x1a\x1dstreamlit/proto/Element.proto\x1a\"streamlit/proto/NamedDataSet.proto\x1a\'streamlit/proto/ArrowNamedDataSet.proto\"\x9e\x01\n\x05\x44\x65lta\x12\x1f\n\x0bnew_element\x18\x03 \x01(\x0b\x32\x08.ElementH\x00\x12\x1b\n\tadd_block\x18\x06 \x01(\x0b\x32\x06.BlockH\x00\x12!\n\x08\x61\x64\x64_rows\x18\x05 \x01(\x0b\x32\r.NamedDataSetH\x00\x12,\n\x0e\x61rrow_add_rows\x18\x07 \x01(\x0b\x32\x12.ArrowNamedDataSetH\x00\x42\x06\n\x04typeb\x06proto3')
  ,
  dependencies=[streamlit_dot_proto_dot_Block__pb2.DESCRIPTOR,streamlit_dot_proto_dot_Element__pb2.DESCRIPTOR,streamlit_dot_proto_dot_NamedDataSet__pb2.DESCRIPTOR,streamlit_dot_proto_dot_ArrowNamedDataSet__pb2.DESCRIPTOR,])




_DELTA = _descriptor.Descriptor(
  name='Delta',
  full_name='Delta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='new_element', full_name='Delta.new_element', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='add_block', full_name='Delta.add_block', index=1,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='add_rows', full_name='Delta.add_rows', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arrow_add_rows', full_name='Delta.arrow_add_rows', index=3,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type', full_name='Delta.type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=169,
  serialized_end=327,
)

_DELTA.fields_by_name['new_element'].message_type = streamlit_dot_proto_dot_Element__pb2._ELEMENT
_DELTA.fields_by_name['add_block'].message_type = streamlit_dot_proto_dot_Block__pb2._BLOCK
_DELTA.fields_by_name['add_rows'].message_type = streamlit_dot_proto_dot_NamedDataSet__pb2._NAMEDDATASET
_DELTA.fields_by_name['arrow_add_rows'].message_type = streamlit_dot_proto_dot_ArrowNamedDataSet__pb2._ARROWNAMEDDATASET
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['new_element'])
_DELTA.fields_by_name['new_element'].containing_oneof = _DELTA.oneofs_by_name['type']
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['add_block'])
_DELTA.fields_by_name['add_block'].containing_oneof = _DELTA.oneofs_by_name['type']
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['add_rows'])
_DELTA.fields_by_name['add_rows'].containing_oneof = _DELTA.oneofs_by_name['type']
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['arrow_add_rows'])
_DELTA.fields_by_name['arrow_add_rows'].containing_oneof = _DELTA.oneofs_by_name['type']
DESCRIPTOR.message_types_by_name['Delta'] = _DELTA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Delta = _reflection.GeneratedProtocolMessageType('Delta', (_message.Message,), dict(
  DESCRIPTOR = _DELTA,
  __module__ = 'streamlit.proto.Delta_pb2'
  # @@protoc_insertion_point(class_scope:Delta)
  ))
_sym_db.RegisterMessage(Delta)


# @@protoc_insertion_point(module_scope)
