"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cproofs.proto\x12\x0fcosmos.ics23.v1"{\n\x0eExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12%\n\x04leaf\x18\x03 \x01(\x0b2\x17.cosmos.ics23.v1.LeafOp\x12&\n\x04path\x18\x04 \x03(\x0b2\x18.cosmos.ics23.v1.InnerOp"\x7f\n\x11NonExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12-\n\x04left\x18\x02 \x01(\x0b2\x1f.cosmos.ics23.v1.ExistenceProof\x12.\n\x05right\x18\x03 \x01(\x0b2\x1f.cosmos.ics23.v1.ExistenceProof"\xef\x01\n\x0fCommitmentProof\x120\n\x05exist\x18\x01 \x01(\x0b2\x1f.cosmos.ics23.v1.ExistenceProofH\x00\x126\n\x08nonexist\x18\x02 \x01(\x0b2".cosmos.ics23.v1.NonExistenceProofH\x00\x12,\n\x05batch\x18\x03 \x01(\x0b2\x1b.cosmos.ics23.v1.BatchProofH\x00\x12;\n\ncompressed\x18\x04 \x01(\x0b2%.cosmos.ics23.v1.CompressedBatchProofH\x00B\x07\n\x05proof"\xc8\x01\n\x06LeafOp\x12%\n\x04hash\x18\x01 \x01(\x0e2\x17.cosmos.ics23.v1.HashOp\x12,\n\x0bprehash_key\x18\x02 \x01(\x0e2\x17.cosmos.ics23.v1.HashOp\x12.\n\rprehash_value\x18\x03 \x01(\x0e2\x17.cosmos.ics23.v1.HashOp\x12)\n\x06length\x18\x04 \x01(\x0e2\x19.cosmos.ics23.v1.LengthOp\x12\x0e\n\x06prefix\x18\x05 \x01(\x0c"P\n\x07InnerOp\x12%\n\x04hash\x18\x01 \x01(\x0e2\x17.cosmos.ics23.v1.HashOp\x12\x0e\n\x06prefix\x18\x02 \x01(\x0c\x12\x0e\n\x06suffix\x18\x03 \x01(\x0c"\x8d\x01\n\tProofSpec\x12*\n\tleaf_spec\x18\x01 \x01(\x0b2\x17.cosmos.ics23.v1.LeafOp\x12.\n\ninner_spec\x18\x02 \x01(\x0b2\x1a.cosmos.ics23.v1.InnerSpec\x12\x11\n\tmax_depth\x18\x03 \x01(\x05\x12\x11\n\tmin_depth\x18\x04 \x01(\x05"\xa6\x01\n\tInnerSpec\x12\x13\n\x0bchild_order\x18\x01 \x03(\x05\x12\x12\n\nchild_size\x18\x02 \x01(\x05\x12\x19\n\x11min_prefix_length\x18\x03 \x01(\x05\x12\x19\n\x11max_prefix_length\x18\x04 \x01(\x05\x12\x13\n\x0bempty_child\x18\x05 \x01(\x0c\x12%\n\x04hash\x18\x06 \x01(\x0e2\x17.cosmos.ics23.v1.HashOp":\n\nBatchProof\x12,\n\x07entries\x18\x01 \x03(\x0b2\x1b.cosmos.ics23.v1.BatchEntry"\x7f\n\nBatchEntry\x120\n\x05exist\x18\x01 \x01(\x0b2\x1f.cosmos.ics23.v1.ExistenceProofH\x00\x126\n\x08nonexist\x18\x02 \x01(\x0b2".cosmos.ics23.v1.NonExistenceProofH\x00B\x07\n\x05proof"\x7f\n\x14CompressedBatchProof\x126\n\x07entries\x18\x01 \x03(\x0b2%.cosmos.ics23.v1.CompressedBatchEntry\x12/\n\rlookup_inners\x18\x02 \x03(\x0b2\x18.cosmos.ics23.v1.InnerOp"\x9d\x01\n\x14CompressedBatchEntry\x12:\n\x05exist\x18\x01 \x01(\x0b2).cosmos.ics23.v1.CompressedExistenceProofH\x00\x12@\n\x08nonexist\x18\x02 \x01(\x0b2,.cosmos.ics23.v1.CompressedNonExistenceProofH\x00B\x07\n\x05proof"k\n\x18CompressedExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12%\n\x04leaf\x18\x03 \x01(\x0b2\x17.cosmos.ics23.v1.LeafOp\x12\x0c\n\x04path\x18\x04 \x03(\x05"\x9d\x01\n\x1bCompressedNonExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x127\n\x04left\x18\x02 \x01(\x0b2).cosmos.ics23.v1.CompressedExistenceProof\x128\n\x05right\x18\x03 \x01(\x0b2).cosmos.ics23.v1.CompressedExistenceProof*e\n\x06HashOp\x12\x0b\n\x07NO_HASH\x10\x00\x12\n\n\x06SHA256\x10\x01\x12\n\n\x06SHA512\x10\x02\x12\n\n\x06KECCAK\x10\x03\x12\r\n\tRIPEMD160\x10\x04\x12\x0b\n\x07BITCOIN\x10\x05\x12\x0e\n\nSHA512_256\x10\x06*\xab\x01\n\x08LengthOp\x12\r\n\tNO_PREFIX\x10\x00\x12\r\n\tVAR_PROTO\x10\x01\x12\x0b\n\x07VAR_RLP\x10\x02\x12\x0f\n\x0bFIXED32_BIG\x10\x03\x12\x12\n\x0eFIXED32_LITTLE\x10\x04\x12\x0f\n\x0bFIXED64_BIG\x10\x05\x12\x12\n\x0eFIXED64_LITTLE\x10\x06\x12\x14\n\x10REQUIRE_32_BYTES\x10\x07\x12\x14\n\x10REQUIRE_64_BYTES\x10\x08B"Z github.com/cosmos/ics23/go;ics23b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proofs_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z github.com/cosmos/ics23/go;ics23'
    _HASHOP._serialized_start = 1874
    _HASHOP._serialized_end = 1975
    _LENGTHOP._serialized_start = 1978
    _LENGTHOP._serialized_end = 2149
    _EXISTENCEPROOF._serialized_start = 33
    _EXISTENCEPROOF._serialized_end = 156
    _NONEXISTENCEPROOF._serialized_start = 158
    _NONEXISTENCEPROOF._serialized_end = 285
    _COMMITMENTPROOF._serialized_start = 288
    _COMMITMENTPROOF._serialized_end = 527
    _LEAFOP._serialized_start = 530
    _LEAFOP._serialized_end = 730
    _INNEROP._serialized_start = 732
    _INNEROP._serialized_end = 812
    _PROOFSPEC._serialized_start = 815
    _PROOFSPEC._serialized_end = 956
    _INNERSPEC._serialized_start = 959
    _INNERSPEC._serialized_end = 1125
    _BATCHPROOF._serialized_start = 1127
    _BATCHPROOF._serialized_end = 1185
    _BATCHENTRY._serialized_start = 1187
    _BATCHENTRY._serialized_end = 1314
    _COMPRESSEDBATCHPROOF._serialized_start = 1316
    _COMPRESSEDBATCHPROOF._serialized_end = 1443
    _COMPRESSEDBATCHENTRY._serialized_start = 1446
    _COMPRESSEDBATCHENTRY._serialized_end = 1603
    _COMPRESSEDEXISTENCEPROOF._serialized_start = 1605
    _COMPRESSEDEXISTENCEPROOF._serialized_end = 1712
    _COMPRESSEDNONEXISTENCEPROOF._serialized_start = 1715
    _COMPRESSEDNONEXISTENCEPROOF._serialized_end = 1872