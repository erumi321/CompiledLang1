import string
import struct

#Decodes 1 byte to a uint
def DecodeUInt8(inp):
    return int.from_bytes(inp, "little", signed=False)

#Decodes 4 bytes to a uint
def DecodeUInt32(inp):
    return int.from_bytes(inp, "little", signed=False)

#Decodes 4 bytes to a signed integer
def DecodeInt32(inp):
    return int.from_bytes(inp, "little", signed=True)

#Encodes an 8-bit uint into binary
def EncodeUInt8(val):
    if val < 0 or val > 255:
        return -1
    return struct.pack("<i", val)

#Encodes a 32-bit uint into binary
def EncodeUInt32(val):
    if val < 0 or val > 4294967295:
        return -1
    return struct.pack("<i", val)

#Encodes a 32-bit int into binary
def EncodeInt32(val):
    if abs(val) > 2147483647:
        return -1 
    return struct.pack("<i", val)

#Decodes bytes into a string (does not use the length bytes, that must be handled elsewhere)
def DecodeString(inp):
    output = ""
    for c in inp:
        i = DecodeUInt8(c)
        output = output + str(i)

    return output

#Encode a string into bytes
def EncodeString(inp):
    b = EncodeUInt32(len(string))

    for c in inp:
        b.append(EncodeUInt32(ord(c)))

    return b