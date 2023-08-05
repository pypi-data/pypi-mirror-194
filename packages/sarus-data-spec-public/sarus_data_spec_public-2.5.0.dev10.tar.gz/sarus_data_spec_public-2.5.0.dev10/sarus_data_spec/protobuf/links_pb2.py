# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sarus_data_spec/protobuf/links.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from sarus_data_spec.protobuf import path_pb2 as sarus__data__spec_dot_protobuf_dot_path__pb2
from sarus_data_spec.protobuf import statistics_pb2 as sarus__data__spec_dot_protobuf_dot_statistics__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='sarus_data_spec/protobuf/links.proto',
  package='sarus_data_spec',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$sarus_data_spec/protobuf/links.proto\x12\x0fsarus_data_spec\x1a#sarus_data_spec/protobuf/path.proto\x1a)sarus_data_spec/protobuf/statistics.proto\"\xdb\x03\n\x05Links\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x61taset\x18\x02 \x01(\t\x12\x39\n\x10links_statistics\x18\x03 \x03(\x0b\x32\x1f.sarus_data_spec.Links.LinkStat\x12:\n\nproperties\x18\x04 \x03(\x0b\x32&.sarus_data_spec.Links.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x88\x02\n\x08LinkStat\x12\'\n\x08pointing\x18\x01 \x01(\x0b\x32\x15.sarus_data_spec.Path\x12&\n\x07pointed\x18\x02 \x01(\x0b\x32\x15.sarus_data_spec.Path\x12\x33\n\x0c\x64istribution\x18\x03 \x01(\x0b\x32\x1d.sarus_data_spec.Distribution\x12\x43\n\nproperties\x18\x04 \x03(\x0b\x32/.sarus_data_spec.Links.LinkStat.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3'
  ,
  dependencies=[sarus__data__spec_dot_protobuf_dot_path__pb2.DESCRIPTOR,sarus__data__spec_dot_protobuf_dot_statistics__pb2.DESCRIPTOR,])




_LINKS_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='sarus_data_spec.Links.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='sarus_data_spec.Links.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='sarus_data_spec.Links.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=297,
  serialized_end=346,
)

_LINKS_LINKSTAT_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='sarus_data_spec.Links.LinkStat.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='sarus_data_spec.Links.LinkStat.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='sarus_data_spec.Links.LinkStat.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=297,
  serialized_end=346,
)

_LINKS_LINKSTAT = _descriptor.Descriptor(
  name='LinkStat',
  full_name='sarus_data_spec.Links.LinkStat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pointing', full_name='sarus_data_spec.Links.LinkStat.pointing', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pointed', full_name='sarus_data_spec.Links.LinkStat.pointed', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='distribution', full_name='sarus_data_spec.Links.LinkStat.distribution', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='sarus_data_spec.Links.LinkStat.properties', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LINKS_LINKSTAT_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=349,
  serialized_end=613,
)

_LINKS = _descriptor.Descriptor(
  name='Links',
  full_name='sarus_data_spec.Links',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='sarus_data_spec.Links.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dataset', full_name='sarus_data_spec.Links.dataset', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='links_statistics', full_name='sarus_data_spec.Links.links_statistics', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='sarus_data_spec.Links.properties', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LINKS_PROPERTIESENTRY, _LINKS_LINKSTAT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=613,
)

_LINKS_PROPERTIESENTRY.containing_type = _LINKS
_LINKS_LINKSTAT_PROPERTIESENTRY.containing_type = _LINKS_LINKSTAT
_LINKS_LINKSTAT.fields_by_name['pointing'].message_type = sarus__data__spec_dot_protobuf_dot_path__pb2._PATH
_LINKS_LINKSTAT.fields_by_name['pointed'].message_type = sarus__data__spec_dot_protobuf_dot_path__pb2._PATH
_LINKS_LINKSTAT.fields_by_name['distribution'].message_type = sarus__data__spec_dot_protobuf_dot_statistics__pb2._DISTRIBUTION
_LINKS_LINKSTAT.fields_by_name['properties'].message_type = _LINKS_LINKSTAT_PROPERTIESENTRY
_LINKS_LINKSTAT.containing_type = _LINKS
_LINKS.fields_by_name['links_statistics'].message_type = _LINKS_LINKSTAT
_LINKS.fields_by_name['properties'].message_type = _LINKS_PROPERTIESENTRY
DESCRIPTOR.message_types_by_name['Links'] = _LINKS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Links = _reflection.GeneratedProtocolMessageType('Links', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _LINKS_PROPERTIESENTRY,
    '__module__' : 'sarus_data_spec.protobuf.links_pb2'
    # @@protoc_insertion_point(class_scope:sarus_data_spec.Links.PropertiesEntry)
    })
  ,

  'LinkStat' : _reflection.GeneratedProtocolMessageType('LinkStat', (_message.Message,), {

    'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
      'DESCRIPTOR' : _LINKS_LINKSTAT_PROPERTIESENTRY,
      '__module__' : 'sarus_data_spec.protobuf.links_pb2'
      # @@protoc_insertion_point(class_scope:sarus_data_spec.Links.LinkStat.PropertiesEntry)
      })
    ,
    'DESCRIPTOR' : _LINKS_LINKSTAT,
    '__module__' : 'sarus_data_spec.protobuf.links_pb2'
    # @@protoc_insertion_point(class_scope:sarus_data_spec.Links.LinkStat)
    })
  ,
  'DESCRIPTOR' : _LINKS,
  '__module__' : 'sarus_data_spec.protobuf.links_pb2'
  # @@protoc_insertion_point(class_scope:sarus_data_spec.Links)
  })
_sym_db.RegisterMessage(Links)
_sym_db.RegisterMessage(Links.PropertiesEntry)
_sym_db.RegisterMessage(Links.LinkStat)
_sym_db.RegisterMessage(Links.LinkStat.PropertiesEntry)


_LINKS_PROPERTIESENTRY._options = None
_LINKS_LINKSTAT_PROPERTIESENTRY._options = None
# @@protoc_insertion_point(module_scope)
