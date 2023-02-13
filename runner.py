from stack_manager import StackManager
from error_handler import ErrorHandler
from binary_helper import *
import sys
import time

eH = ErrorHandler()

stacks = StackManager(eH)

SIGNIFIER_BYTES = {
    0: "clr",
    1: "psh",
    2: "del",
    3: "sze",
    4: "prt",
    5: "psl",
    6: "mov",
    7: "add",
    8: "sub",
    9: "inc",
    10: "dec",
    11: "mlt",
    12: "div",
    13: "eql",
    14: "grt",
    15: "jmp",
    16: "not",
    17: "lsr",
    18: "inp",
    19: "inp_alt",
    20: "nin",
    21: "nin_alt",
    22: "slp"
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

def PrintSameLineFromStack(f):
    if not ErrorHandler.has_done_error:
        stack_num = DecodeUInt32(f.read(4))
        print(stacks.get_stack_val(stack_num), end="")
        sys.stdout.flush()

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

    val = stacks.get_stack_val_force_type(input_stacknum1, float) + stacks.get_stack_val_force_type(input_stacknum2, float)

    stacks.push_stack(target_stacknum, val)

def SubBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, float) - stacks.get_stack_val_force_type(input_stacknum2, float)

    stacks.push_stack(target_stacknum, val)

def IncreaseStack(f):
    stack_num = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(stack_num, float) + 1

    stacks.pop_stack(stack_num)
    stacks.push_stack(stack_num, val)

def DecreaseStack(f):
    stack_num = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(stack_num, float) - 1

    stacks.pop_stack(stack_num)
    stacks.push_stack(stack_num, val)

def MultiplyBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(input_stacknum1, float) * stacks.get_stack_val_force_type(input_stacknum2, float)

    stacks.push_stack(target_stacknum, val)

def DivideBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    val_1 = stacks.get_stack_val_force_type(input_stacknum1, float)
    val_2 = stacks.get_stack_val_force_type(input_stacknum2, float)

    val = val_1

    if val_2 == 0:
        eH.ThrowError("Divide by zero")
    else:
        val = val_1 / val_2

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

    value_1 = stacks.get_stack_val_force_type(input_stacknum1, float)
    value_2 = stacks.get_stack_val_force_type(input_stacknum2, float)

    if value_1 > value_2:
        stacks.push_stack(target_stacknum, 1)
    else:
        stacks.push_stack(target_stacknum, 0)

def LesserBetweenStacks(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    input_stacknum2 = DecodeUInt32(f.read(4))
    target_stacknum = DecodeUInt32(f.read(4))

    value_1 = stacks.get_stack_val_force_type(input_stacknum1, float)
    value_2 = stacks.get_stack_val_force_type(input_stacknum2, float)

    if value_1 < value_2:
        stacks.push_stack(target_stacknum, 1)
    else:
        stacks.push_stack(target_stacknum, 0)

def JumpLine(f):
    input_stacknum1 = DecodeUInt32(f.read(4))
    byte_pos = DecodeUInt32(f.read(4))

    line_num = DecodeUInt32(f.read(4))

    value_1 = stacks.get_stack_val_force_type(input_stacknum1, float)

    if value_1 != 0:
        return [byte_pos, line_num]

def NotStack(f):
    target_stack = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(target_stack, float)

    if val != 0 and val != 1:
        eH.ThrowError("Incorrect operation for Not, cannot swap a non-boolean value (1 or 0)")
    
    n_val = 0

    if val == 0:
        n_val = 1

    stacks.pop_stack(target_stack)
    stacks.push_stack(target_stack, n_val)

def InputToStack(f):
    target_stack = DecodeUInt32(f.read(4))

    value = input(">")

    stacks.push_stack(target_stack, value)

def PromptInputToStack(f):
    prompt_stack = DecodeUInt32(f.read(4))
    target_stack = DecodeUInt32(f.read(4))

    prompt = stacks.get_stack_val(prompt_stack)
    value = input(str(prompt))

    print('value:', value)
    print('target:', target_stack)


    stacks.push_stack(target_stack, value)

def InputNumberToStack(f):
    target_stack = DecodeUInt32(f.read(4))

    while True:
        try:
            value = value = input("(Number Input) >")
            value = float(value)
            break
        except ValueError:
            print("Incorrect - this requires a number, please try again: ")
    
    stacks.push_stack(target_stack, value)

def PromptInputNumberToStack(f):
    prompt_stack = DecodeUInt32(f.read(4))
    target_stack = DecodeUInt32(f.read(4))

    prompt = stacks.get_stack_val(prompt_stack)
    
    while True:
        try:
            value = input("(Number Input) " + str(prompt) + " ")
            value = float(value)
            break
        except ValueError:
            print("Incorrect - this requires a number, please try again: ")

    stacks.push_stack(target_stack, value)

def SleepFromStack(f):
    target_stack = DecodeUInt32(f.read(4))

    val = stacks.get_stack_val_force_type(target_stack, float)

    time.sleep(val / 1000)

COMMAND_MAP = {
    "clr": ClearStack,
    "psh": PushToStack,
    "del": DeleteFromStack,
    "sze": PushStackSizeOntoStack,
    "prt": PrintFromStack,
    "psl": PrintSameLineFromStack,
    "mov": MoveStack,
    "add": AddBetweenStacks,
    "sub": SubBetweenStacks,
    "inc": IncreaseStack,
    "dec": DecreaseStack,
    "mlt": MultiplyBetweenStacks,
    "div": DivideBetweenStacks,
    "eql": EqualBetweenStacks,
    "grt": GreaterBetweenStacks,
    "jmp": JumpLine,
    "not": NotStack,
    "lsr": LesserBetweenStacks,
    "inp": InputToStack,
    "inp_alt": PromptInputToStack,
    "nin": InputNumberToStack,
    "nin_alt": PromptInputNumberToStack,
    "slp": SleepFromStack
}

def RunLine(line):
    command = line.split(" ")

    COMMAND_MAP[command[0]](command[1:])

line_pos_dict = {}

input_file = "output.cl1"

if len(sys.argv) > 1:
    input_file = str(sys.argv[1]) + ".cl1"


with open(input_file, "rb") as f:
    num_commands = DecodeUInt32(f.read(4))
    i = 1
    while True:
        pos = f.tell()
        next_three = f.read(3)
        if next_three == b'\x7e\x03\x7e':
            break

        i = i + 1
        ErrorHandler.current_line_num = i

        f.seek(pos)

        r = f.read(1)
        t = DecodeUInt8(r)
        ErrorHandler.current_line = SIGNIFIER_BYTES[t]
        x = COMMAND_MAP[SIGNIFIER_BYTES[t]](f)
        if x is not None:
            f.seek(x[0])
            i = x[1]
        
    
    print("")