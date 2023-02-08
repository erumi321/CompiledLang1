from stack_manager import StackManager
from error_handler import ErrorHandler
from binary_helper import *

eH = ErrorHandler()

stacks = StackManager(eH)

SIGNIFIER_BYTES = {
    0: "c",
    1: "psh",
    2: "del",
    3: "sze",
    4: "prt",
    6: "mov",
    7: "add",
    8: "sub",
    9: "inc",
    10: "dec",
    11: "mlt",
    12: "div",
    13: "eql",
    14: "grt"
}

def ClearStack(f):
    stack_num = DecodeUInt32(f.read(4))
    stacks.clear_stack(stack_num)

def PushToStack(f):
    str_len = DecodeUInt32(f.read(4))
    str_val = DecodeString(f.read(str_len))
    stack_num = DecodeUInt32(f.read(4))

    stacks.push_stack(stack_num, str_val)

def DeleteFromStack(f):
    stack_num = DecodeUInt32(f.read(4))
    stacks.pop_stack(stack_num)

def PushStackSizeOntoStack(f):
    stack_num = DecodeUInt32(f.read(4))
    length = stacks.stack_length(stack_num)
    stacks.push_stack(stack_num, length)

def PrintFromStack(f):
    if not ErrorHandler.has_done_error:
        stack_num = DecodeUInt32(f.read(4))
        print(stacks.get_stack_val(stack_num))

def MoveStack(f):
    input_stacknum = DecodeUInt32(f.read(4))
    output_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val(input_stacknum)
    stacks.push_stack(output_stacknum, val)

    stacks.pop_stack(input_stacknum)

def AddBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, int) + stacks.get_stack_val_force_type(input_stacknum2, int)

    stacks.push_stack(target_stacknum, val)

def SubBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, int) - stacks.get_stack_val_force_type(input_stacknum2, int)

    stacks.push_stack(target_stacknum, val)

def IncreaseStack(f):
    stack_num = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(stack_num, int) + 1

    stacks.pop_stack(stack_num)
    stacks.push_stack(stack_num, val)

def DecreaseStack(f):
    stack_num = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(stack_num, int) - 1

    stacks.pop_stack(stack_num)
    stacks.push_stack(stack_num, val)

def MultiplyBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, int) * stacks.get_stack_val_force_type(input_stacknum2, int)

    stacks.push_stack(target_stacknum, val)

def DivideBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, int) // stacks.get_stack_val_force_type(input_stacknum2, int)

    stacks.push_stack(target_stacknum, val)

def EqualBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    value_1 = stacks.get_stack_val(input_stacknum1)
    value_2 = stacks.get_stack_val(input_stacknum2)

    try:
        i_v1 = int(value_1)
        i_v2 = int(value_2)
        
        if i_v1 == i_v2:
            stacks.push_stack(target_stacknum, 1)
        else:
            stacks.push_stack(target_stacknum, 0)
    except:
        if value_1 == value_2:
            stacks.push_stack(target_stacknum, 1)
        else:
            stacks.push_stack(target_stacknum, 0)

def GreaterBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    value_1 = stacks.get_stack_val_force_type(input_stacknum1, int)
    value_2 = stacks.get_stack_val_force_type(input_stacknum2, int)

    if value_1 > value_2:
        stacks.push_stack(target_stacknum, 1)
    else:
        stacks.push_stack(target_stacknum, 0)

COMMAND_MAP = {
    "c": ClearStack,
    "psh": PushToStack,
    "del": DeleteFromStack,
    "sze": PushStackSizeOntoStack,
    "prt": PrintFromStack,
    "mov": MoveStack,
    "add": AddBetweenStacks,
    "sub": SubBetweenStacks,
    "inc": IncreaseStack,
    "dec": DecreaseStack,
    "mlt": MultiplyBetweenStacks,
    "div": DivideBetweenStacks,
    "eql": EqualBetweenStacks,
    "grt": GreaterBetweenStacks
}

def RunLine(line):
    command = line.split(" ")

    COMMAND_MAP[command[0]](command[1:])

with open("output.cl1", "rb") as f:
    num_commands = DecodeUInt32(f.read(4))
    for i in range(num_commands):
        ErrorHandler.current_line_num = i + 1
        t = DecodeUInt8(f.read(1))

        COMMAND_MAP[SIGNIFIER_BYTES[t]](f)