# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: product.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\"l\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x02\x12\"\n\x08\x63\x61tegory\x18\x05 \x01(\x0e\x32\x10.ProductCategory\"8\n\x12ProductListRequest\x12\"\n\x08\x63\x61tegory\x18\x01 \x01(\x0e\x32\x10.ProductCategory\"1\n\x13ProductListResponse\x12\x1a\n\x08products\x18\x01 \x03(\x0b\x32\x08.Product*5\n\x0fProductCategory\x12\n\n\x06MOBILE\x10\x00\x12\n\n\x06LAPTOP\x10\x01\x12\n\n\x06\x43\x41MERA\x10\x02\x32J\n\x0eProductService\x12\x38\n\x0bGetProducts\x12\x13.ProductListRequest\x1a\x14.ProductListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTCATEGORY']._serialized_start=236
  _globals['_PRODUCTCATEGORY']._serialized_end=289
  _globals['_PRODUCT']._serialized_start=17
  _globals['_PRODUCT']._serialized_end=125
  _globals['_PRODUCTLISTREQUEST']._serialized_start=127
  _globals['_PRODUCTLISTREQUEST']._serialized_end=183
  _globals['_PRODUCTLISTRESPONSE']._serialized_start=185
  _globals['_PRODUCTLISTRESPONSE']._serialized_end=234
  _globals['_PRODUCTSERVICE']._serialized_start=291
  _globals['_PRODUCTSERVICE']._serialized_end=365
# @@protoc_insertion_point(module_scope)
