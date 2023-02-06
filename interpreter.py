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

COMMAND_MAP = {
    "c": ClearStack,
    "psh": PushToStack,
    "del": DeleteFromStack,
    "sze": PushStackSizeOntoStack,
    "prt": PrintFromStack,
    # if 
    # for
    # fnc
    # cll
}

def RunLine(line):
    command = line.split(" ")

    COMMAND_MAP[command[0]](command[1:])

with open("output.cl1", "rb") as f:
    num_commands = DecodeUInt32(f.read(4))
    for i in range(num_commands):
        t = DecodeUInt8(f.read(1))

        COMMAND_MAP[SIGNIFIER_BYTES[t]](f)