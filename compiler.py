from binary_helper import *
from error_handler import ErrorHandler

eH = ErrorHandler()

SIGNIFIER_BYTES = {
    "c": 0,
    "psh": 1,
    "del": 2,
    "sze": 3,
    "prt": 4,
}

def encode_clear(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for clear, found" + str(len(args)) + " expecting 1")
        return b""
    return EncodeUInt32(args[1])

def encode_push(args):
    if len(args) < 1:
        eH.ThrowError("Incorrect number of arguments for push, found" + str(len(args)) + " expecting > 1")
        return b""
    value = ""
    for arg in args:
        value = value + arg + " "

    value = value[0:-1]
    value_bytes = EncodeString(value)

    return value_bytes 

def encode_delete(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for delete, found" + str(len(args)) + " expecting 1")
        return b""
    return EncodeUInt32(args[1])

def encode_size(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for size, found" + str(len(args)) + " expecting 1")
        return b""
    return EncodeUInt32(args[1])

def encode_print(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for print, found" + str(len(args)) + " expecting 1")
        return b""
    return EncodeUInt32(args[1])


ENCODING_FUNCTIONS = {
    "c": encode_clear,
    "psh": encode_push,
    "del": encode_delete,
    "sze": encode_size,
    "prt": encode_print
}

def encode_line(line):
    command = line.split(" ")

    if not command[0] in SIGNIFIER_BYTES:
        eH.ThrowError("Incorrect Command")

    sig_byte = EncodeUInt8(SIGNIFIER_BYTES[command[0]])

    body_bytes = ENCODING_FUNCTIONS[command[0]](command[1:-1])

    print(sig_byte)
    return sig_byte + body_bytes

with open("input.txt", "r", encoding="utf-8") as r:
    output_bytes = b""

    lines = r.read().split("\n")

    #num commands bytes
    output_bytes = output_bytes + EncodeUInt32(len(lines))

    line_num = 0
    for line in lines:
        line_num = line_num + 1
        if len(line.strip()) == 0:
            continue
        ErrorHandler.current_line_num = line_num
        output_bytes = output_bytes + encode_line(line.strip())
    
    with open("output.cl1", "wb") as w:
        w.write(output_bytes)