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
        eH.ThrowError("Incorrect number of arguments for clear, found " + str(len(args)) + " expected 1")
        return b""
    try:
        i = int(args[0])
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for clear, expected int")
        return b""

def encode_push(args):
    if len(args) < 1:
        eH.ThrowError("Incorrect number of arguments for push, found " + str(len(args)) + " expected > 1")
        return b""
    value = ""
    for i in range(len(args) - 1):
        arg = args[i]
        value = value + arg + " "

    value = value[0:-1]
    value_bytes = EncodeString(value)

    try:
        stack_bytes = EncodeUInt32(int(args[len(args) - 1]))
        return value_bytes + stack_bytes
    except ValueError:
        eH.ThrowError("Incorrect type of argument for stack number for push, expected int")
        return b""    

def encode_delete(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for delete, found " + str(len(args)) + " expected 1")
        return b""
    try:
        i = int(args[0])
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for delete, expected int")
        return b""

def encode_size(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for size, found " + str(len(args)) + " expected 1")
        return b""
    try:
        i = int(args[0])
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for size, expected int")
        return b""

def encode_print(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for print, found " + str(len(args)) + " expected 1")
        return b""
    try:
        i = int(args[0])
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for clear, expected int")
        return b""


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

    body_bytes = ENCODING_FUNCTIONS[command[0]](command[1:])

    print(sig_byte)
    print(body_bytes)
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
    
    if not ErrorHandler.has_done_error:
        with open("output.cl1", "wb") as w:
            w.write(output_bytes)