from binary_helper import *
from error_handler import ErrorHandler
from stack_manager import StackManager
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
    "inp_alt": 19,
    "inn": 20,
    "inn_alt": 21,
    "slp": 22
}

output_bytes = b""

line_num_to_bytes=  {}

queued_jumps = []
mark_locations = {}
line_num = 0

stacks = StackManager(eH)

def encode_clear(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for clear, found " + str(len(args)) + " expected 1")
    i = 0
    try:
        i = int(args[0])
        stacks.clear_stack(i)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of clear, expected int")

    return EncodeUInt32(i)

def encode_push(args):
    if len(args) < 1:
        eH.ThrowError("Incorrect number of arguments for psh, found " + str(len(args)) + " expected > 1")

    value = ""
    for i in range(len(args) - 1):
        arg = args[i]
        value = value + arg + " "

    value = value[0:-1]
    value_bytes = EncodeString(value)

    stack_bytes = b""
    try:
        i = int(args[len(args) - 1])
        stack_bytes = EncodeUInt32(i)
        stacks.push_stack(i, value)
    except ValueError:
        eH.ThrowError("Incorrect type for final argument (stack number) of psh, expected int")  
    return value_bytes + stack_bytes

def encode_delete(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for delete, found " + str(len(args)) + " expected 1")
    i = 0
    try:
        i = int(args[0])
        if not stacks.bool_stack_exists(i) or stacks.stack_length(i) == 0:
            eH.ThrowError("Trying to delete value from an empty stack (", i, ")")
        else:
            stacks.pop_stack(i)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of delete, expected int")
        return b""
    return EncodeUInt32(i)

def encode_size(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for sze, found " + str(len(args)) + " expected 1")
    i = 0
    try:
        i = int(args[0])
        if not stacks.bool_stack_exists(i) or stacks.stack_length(i) == 0:
            eH.ThrowError("Trying to get size of empty stack (", i, ")")
        else:
            stacks.push_stack(i, stacks.stack_length(i))
    except ValueError:
        eH.ThrowError("Incorrect type fpr argument 1 of sze, expected int")
    return EncodeUInt32(i)

def encode_print(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for prt, found " + str(len(args)) + " expected 1")
    i = 0
    try:
        i = int(args[0])
        if not stacks.bool_stack_exists(i) or stacks.stack_length(i) == 0:
            eH.ThrowError("Trying to print value from an empty stack (", i, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of prt, expected int")
    return EncodeUInt32(i)
    
def encode_print_same_line(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for psl, found " + str(len(args)) + " expected 1")
    try:
        i = int(args[0])
        if not stacks.bool_stack_exists(i) or stacks.stack_length(i) == 0:
            eH.ThrowError("Trying to print value from an empty stack (", i, ")")
        return EncodeUInt32(i)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of psl, expected int")

def encode_move(args):
    if len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for mov, found " + str(len(args)) + " expected 2")
    stack_1 = 0
    stack_2 = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to move value off of empty stack (", stack_1, ")")
        else:
           stacks.pop_stack(stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of mov, expected int")
    try:
        stack_2 = int(args[1])
        stacks.push_stack(stack_2, 1)

    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of mov, expected int")

    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2)

def encode_add(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for add, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to add value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to add by non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of add, expected int")

    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to add value of empty stack (", stack_2, ")")
        if stacks.get_stack_val_force_type(stack_2, float) == ValueError:
            eH.ThrowError("Tyring to add by non-number value on stack ", stack_2)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of add, expected int")

    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of add, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_sub(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for sub, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to subtract value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to subtract by non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of sub, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to subtract value of empty stack (", stack_2, ")")
        if stacks.get_stack_val_force_type(stack_2, float) == ValueError:
            eH.ThrowError("Tyring to subtract by non-number value on stack ", stack_2)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of sub, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of sub, expected int")

    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_inc(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for inc, found " + str(len(args)) + " expected 1")

    stack_1 = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to increase value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to increase non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of inc, expected int")

    return EncodeUInt32(stack_1)

def encode_dec(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for dec, found " + str(len(args)) + " expected 1")

    stack_1 = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to decrease value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to decrease non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of dec, expected int")

    return EncodeUInt32(stack_1)

def encode_mult(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for mlt, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to multiply value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to multiply by non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of mlt, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to multiply value of empty stack (", stack_2, ")")
        if stacks.get_stack_val_force_type(stack_2, float) == ValueError:
            eH.ThrowError("Tyring to multiply by non-number value on stack ", stack_2)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of mlt, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of mlt, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_divide(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for div, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to divide value of empty stack (", stack_1, ")")
        if stacks.get_stack_val_force_type(stack_1, float) == ValueError:
            eH.ThrowError("Tyring to divide by non-float value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of div, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to divide value of empty stack (", stack_2, ")")
        if stacks.get_stack_val_force_type(stack_2, float) == ValueError:
            eH.ThrowError("Tyring to divide by non-float value on stack ", stack_2)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of div, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of div, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_equal(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for eql, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to check equality of value of empty stack (", stack_1, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of eql, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to check equality of value of empty stack (", stack_2, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of eql, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of eql, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_greater(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for grt, found " + str(len(args)) + " expected 3")

    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to check greater then status of value of empty stack (", stack_1, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of grt, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to check greater then status of value of empty stack (", stack_2, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of grt, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of grt, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_lesser(args):
    if len(args) != 3:
        eH.ThrowError("Incorrect number of arguments for lsr, found " + str(len(args)) + " expected 3")
    stack_1 = 0
    stack_2 = 0
    target_stack = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to check lesser then status of value of empty stack (", stack_1, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of lsr, expected int")
    try:
        stack_2 = int(args[1])
        if not stacks.bool_stack_exists(stack_2) or stacks.stack_length(stack_2) == 0:
            eH.ThrowError("Trying to check lesser then status of value of empty stack (", stack_2, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of lsr, expected int")
    try:
        target_stack = int(args[2])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 3 of lsr, expected int")
    return EncodeUInt32(stack_1) + EncodeUInt32(stack_2) + EncodeUInt32(target_stack)

def encode_jump(args):
    if len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for jmp, found " + str(len(args)) + " expected 2")
    stack_1 = 0
    target = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to check boolean value of empty stack (", stack_1, ")")
        queued_jumps.append([len(output_bytes) + 5, int(args[1])])

    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of jmp, expected int")

    try:
        target = int(args[1])
        if not target in mark_locations:
            eH.ThrowError("Trying to jump to unmarked location ", target)
        queued_jumps.append([len(output_bytes) + 5, target])
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of jmp, expected int")
    
    return EncodeUInt32(stack_1) + EncodeUInt32(0) + EncodeUInt32(0)

def encode_mark(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for mrk, found " + str(len(args)) + " expected 1")
    try:
        value = int(args[0])

        mark_locations[value] = [len(output_bytes), line_num]

    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of mrk, expected int")

    return b""

def encode_not(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for not, found " + str(len(args)) + " expected 1")

    stack_1 = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to perform a not operation on empty stack (", stack_1, ")")
        if not stacks.get_stack_val_force_type(stack_1, float):
            eH.ThrowError("Trying to perform not operation on a non-number value on stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of not, expected int")

    return EncodeUInt32(stack_1)

def encode_input(args):
    if len(args) != 1 and len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for inp, found " + str(len(args)) + " expected 1 or 2")

    target_stack = 0
    try:
        target_stack = int(args[0])
        stacks.push_stack(target_stack, "a")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of inp, expected int")
    return EncodeUInt32(target_stack)

def encode_input_prompt(args):
    prompt_stack = 0
    target_stack = 0
    try:
        prompt_stack = int(args[0])
        if not stacks.bool_stack_exists(prompt_stack) or stacks.stack_length(prompt_stack) == 0:
            eH.ThrowError("Trying to get prompt value off of an empty stack (", prompt_stack, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of inp, expected int")
    try:
        target_stack = int(args[1])
        stacks.push_stack(target_stack, "a")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of inp, expected int")
    return EncodeUInt32(prompt_stack) + EncodeUInt32(target_stack)

def encode_input_number(args):
    if len(args) != 1 and len(args) != 2:
        eH.ThrowError("Incorrect number of arguments for inp, found " + str(len(args)) + " expected 1 or 2")

    target_stack = 0
    try:
        target_stack = int(args[0])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of inp, expected int")
    return EncodeUInt32(target_stack)

def encode_input_number_prompt(args):
    prompt_stack = 0
    target_stack = 0
    try:
        prompt_stack = int(args[0])
        if not stacks.bool_stack_exists(prompt_stack) or stacks.stack_length(prompt_stack) == 0:
            eH.ThrowError("Trying to get prompt value off of an empty stack (", prompt_stack, ")")
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of inp, expected int")
    try:
        target_stack = int(args[1])
        stacks.push_stack(target_stack, 1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 2 of inp, expected int")
    return EncodeUInt32(prompt_stack) + EncodeUInt32(target_stack)

def encode_sleep(args):
    if len(args) != 1:
        eH.ThrowError("Incorrect number of arguments for slp, found " + str(len(args)) + " expected 1")

    stack_1 = 0
    try:
        stack_1 = int(args[0])
        if not stacks.bool_stack_exists(stack_1) or stacks.stack_length(stack_1) == 0:
            eH.ThrowError("Trying to read a sleep value from an empty stack (", stack_1, ")")
        if not stacks.get_stack_val_force_type(stack_1, float):
            eH.ThrowError("Trying to read a non-number for sleep from stack ", stack_1)
    except ValueError:
        eH.ThrowError("Incorrect type for argument 1 of slp, expected int")

    return EncodeUInt32(stack_1)

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
    "inn": encode_input_number,
    "inn_alt": encode_input_number_prompt,
    "mrk": encode_mark,
    "slp": encode_sleep
}

def encode_line(line):
    command = line.split(" ")

    if not command[0] in SIGNIFIER_BYTES and command[0] != "mrk":
        eH.ThrowError("Incorrect Command")

    c = command[0]
    if c == "inp":
        if len(command) == 3:
            c = "inp_alt"
    elif c == "inn":
        if len(command) == 3:
            c = "inn_alt"
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
        command = line.split(" ")

        if command[0] == "mrk":
            if len(command) == 2:
                mark_locations[command[1]] = 0
            else:
                eH.ThrowError("Incorrect number of arguments for mrk, found ", len(command - 1), "expected 1")

    line_num = 0
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