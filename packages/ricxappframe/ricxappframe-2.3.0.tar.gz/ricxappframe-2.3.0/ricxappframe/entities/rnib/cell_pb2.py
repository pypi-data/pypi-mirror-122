# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cell.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import gnb_pb2 as gnb__pb2
from . import enb_pb2 as enb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cell.proto',
  package='entities',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ncell.proto\x12\x08\x65ntities\x1a\tgnb.proto\x1a\tenb.proto\"\xce\x01\n\x04\x43\x65ll\x12!\n\x04type\x18\x01 \x01(\x0e\x32\x13.entities.Cell.Type\x12\x34\n\x10served_cell_info\x18\x02 \x01(\x0b\x32\x18.entities.ServedCellInfoH\x00\x12\x30\n\x0eserved_nr_cell\x18\x03 \x01(\x0b\x32\x16.entities.ServedNRCellH\x00\"3\n\x04Type\x12\x10\n\x0cUNKNOWN_CELL\x10\x00\x12\x0c\n\x08LTE_CELL\x10\x01\x12\x0b\n\x07NR_CELL\x10\x02\x42\x06\n\x04\x63\x65llb\x06proto3')
  ,
  dependencies=[gnb__pb2.DESCRIPTOR,enb__pb2.DESCRIPTOR,])



_CELL_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='entities.Cell.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_CELL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LTE_CELL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NR_CELL', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=194,
  serialized_end=245,
)
_sym_db.RegisterEnumDescriptor(_CELL_TYPE)


_CELL = _descriptor.Descriptor(
  name='Cell',
  full_name='entities.Cell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='entities.Cell.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='served_cell_info', full_name='entities.Cell.served_cell_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='served_nr_cell', full_name='entities.Cell.served_nr_cell', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CELL_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='cell', full_name='entities.Cell.cell',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=47,
  serialized_end=253,
)

_CELL.fields_by_name['type'].enum_type = _CELL_TYPE
_CELL.fields_by_name['served_cell_info'].message_type = enb__pb2._SERVEDCELLINFO
_CELL.fields_by_name['served_nr_cell'].message_type = gnb__pb2._SERVEDNRCELL
_CELL_TYPE.containing_type = _CELL
_CELL.oneofs_by_name['cell'].fields.append(
  _CELL.fields_by_name['served_cell_info'])
_CELL.fields_by_name['served_cell_info'].containing_oneof = _CELL.oneofs_by_name['cell']
_CELL.oneofs_by_name['cell'].fields.append(
  _CELL.fields_by_name['served_nr_cell'])
_CELL.fields_by_name['served_nr_cell'].containing_oneof = _CELL.oneofs_by_name['cell']
DESCRIPTOR.message_types_by_name['Cell'] = _CELL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cell = _reflection.GeneratedProtocolMessageType('Cell', (_message.Message,), dict(
  DESCRIPTOR = _CELL,
  __module__ = 'cell_pb2'
  # @@protoc_insertion_point(class_scope:entities.Cell)
  ))
_sym_db.RegisterMessage(Cell)


# @@protoc_insertion_point(module_scope)
