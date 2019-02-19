import sys
import struct
import json

int64 = 6400
int32 = 3200
int16 = 16

print("int 64: {}".format(sys.getsizeof(int64)))
print("int 32: {}".format(sys.getsizeof(int32)))
print("int 16: {}".format(sys.getsizeof(int16)))

struct_int64 = struct.pack(">Q", int64)
print("struct_int64 size of: {}".format(sys.getsizeof(struct_int64)))
print("struct_int64 len: {}".format(len(struct_int64)))

struct_int32 = struct.pack(">Q", int32)
print("struct_int32 size of: {}".format(sys.getsizeof(struct_int32)))
print("struct_int32 len: {}".format(len(struct_int32)))

struct_int16 = struct.pack(">Q", int16)
print("struct_int16 size of: {}".format(sys.getsizeof(struct_int16)))
print("struct_int16 len: {}".format(len(struct_int16)))


header_size = 8
data_string = json.dumps("Hello this is Python!", ensure_ascii=False).encode("utf-8")
print("Len data string: {}".format(len(data_string)))
header = struct.pack(">Q", len(data_string))
print("Header: {}".format(header))
buffer = header + data_string


header = struct.unpack(">Q", buffer[:header_size])[0]
print("Header: {} (len data string)".format(header))



b = b""

print(b)
print (len(b))