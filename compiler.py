from binary_helper import *
from error_handler import ErrorHandler
import sys

eH = ErrorHandler()

SIGNIFIER_BYTES = {
    "c": 0,
    "psh": 1,
    "del": 2,
    "sze": 3,
    "prt": 4,
    "psl": 5,
    "mov": 6,
    "add": 7,
    "sub": 8,
    "inc": 9,
    "dec": 10,
    "mlt": 11,
    "div": 12,
    "eql": 13,
    "grt": 14,
    "jmp": 15,
    "not": 16,
    "lsr": 17,
    "inp": 18,
    "inp_alt": 19
}

output_bytes = b""

line_num_to_bytes=  {}

queued_jumps = []
mark_locations = {}
line_num = 1

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
    
def encode_print_same_line(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for pls, found " + str(len(args)) + " expected 1")
        return b""
    try:
        i = int(args[0])
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for pls, expected int")
        return b""
def encode_move(args):
    if len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for move, found " + str(len(args)) + " expected 2")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for move, expected int")
        return b""

def encode_add(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for add, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for add, expected int")
        return b""

def encode_sub(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for sub, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for sub, expected int")
        return b""

def encode_inc(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for inc, found " + str(len(args)) + " expected 1")
        return b""
    try:
        stack_1 = int(args[0])
        return EncodeUInt32(stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for inc, expected int")
        return b""

def encode_dec(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for dec, found " + str(len(args)) + " expected 1")
        return b""
    try:
        stack_1 = int(args[0])
        return EncodeUInt32(stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for inc, expected int")
        return b""

def encode_mult(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for mlt, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for mlt, expected int")
        return b""

def encode_divide(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for div, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for div, expected int")
        return b""

def encode_equal(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for eql, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for eql, expected int")
        return b""

def encode_greater(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for grt, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for grt, expected int")
        return b""

def encode_lesser(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for lsr, found " + str(len(args)) + " expected 3")
        return b""
    try:
        stack_1 = int(args[0])
        stack_2 = int(args[1])
        target_stack = int(args[2])
        return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for lsr, expected int")
        return b""

def encode_jump(args):
    if len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for jmp, found " + str(len(args)) + " expected 2")
        return b""
    try:
        stack_1 = int(args[0])

        queued_jumps.append([len(output_bytes) + 5, int(args[1])])

        return EncodeUInt32(stack_1) + EncodeUInt32(0) + EncodeUInt32(0)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for jmp, expected int")
        return b""

def encode_mark(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for mrk, found " + str(len(args)) + " expected 1")
        return b""
    try:
        value = int(args[0])

        mark_locations[value] = [len(output_bytes), line_num]

        return b""
    except ValueError:
        eH.ThrowError("Incorrect type of argument for mrk, expected int")
        return b""

def encode_not(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for not, found " + str(len(args)) + " expected 1")
        return b""
    try:
        stack_1 = int(args[0])
        return EncodeUInt32(stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for not, expected int")
        return b""

def encode_input(args):
    if len(args) != 1 and len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for inp, found " + str(len(args)) + " expected 1 or 2")
        return b""
    try:
        target_stack = int(args[0])
        return EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for inp, expected int")

def encode_input_prompt(args):
    try:
        prompt_stack = int(args[0])
        target_stack = int(args[1])
        return EncodeUInt32(prompt_stack) + EncodeUInt32(target_stack)
    except ValueError:
        eH.ThrowError("Incorrect type of argument for inp, expected int")

ENCODING_FUNCTIONS = {
    "c": encode_clear,
    "psh": encode_push,
    "del": encode_delete,
    "sze": encode_size,
    "prt": encode_print,
    "psl": encode_print_same_line,
    "mov": encode_move,
    "add": encode_add,
    "sub": encode_sub,
    "inc": encode_inc,
    "dec": encode_dec,
    "mlt": encode_mult,
    "div": encode_divide,
    "eql": encode_equal,
    "grt": encode_greater,
    "jmp": encode_jump,
    "not": encode_not,
    "lsr": encode_lesser,
    "inp": encode_input,
    "inp_alt": encode_input_prompt,
    "mrk": encode_mark
}

def encode_line(line):
    command = line.split(" ")

    if not command[0] in SIGNIFIER_BYTES and command[0] != "mrk":
        eH.ThrowError("Incorrect Command")

    c = command[0]
    if c == "inp":
        if len(command) == 3:
            c = "inp_alt"
            print("alt")

    body_bytes = ENCODING_FUNCTIONS[c](command[1:])

    if command[0] != "mrk":
        sig_byte = EncodeUInt8(SIGNIFIER_BYTES[c])
        return sig_byte + body_bytes
    else:
        return b""

input_file = "input.txt"
output_file = "output.cl1"

if len(sys.argv) > 1:
    input_file = str(sys.argv[1]) + ".txt"

if len(sys.argv) > 2:
    output_file = str(sys.argv[2]) + ".cl1"

with open(input_file, "r", encoding="utf-8") as r:
    output_bytes = b""
    lines = r.read().split("\n")

    #num commands bytes
    output_bytes = output_bytes + EncodeUInt32(len(lines))

    for line in lines:
        line_num = line_num + 1
        if len(line.strip()) == 0:
            continue
        ErrorHandler.current_line_num = line_num
        line_num_to_bytes[line_num - 1] = len(output_bytes)

        output_bytes = output_bytes + encode_line(line.strip())

    output_bytes = output_bytes + b'\x7e\x03\x7e'
    if not ErrorHandler.has_done_error:
        with open(output_file, "wb") as w:
            w.write(output_bytes)

            for queued_jump in queued_jumps:
                w.seek(queued_jump[0])

                location = mark_locations[queued_jump[1]][0]
                line_num = mark_locations[queued_jump[1]][1]

                w.write(EncodeUInt32(location))
                w.write(EncodeUInt32(line_num))