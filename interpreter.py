from stack_manager import StackManager
from error_handler import ErrorHandler

eH = ErrorHandler()

stacks = StackManager(eH)

def ClearStack(args):
    stacks.clear_stack(args[0])

def PushToStack(args):
    p_val = args[0] + " "
    if len(args) > 2:
        p_val = ""
        for x in range(0, len(args) - 1):
            p_val = p_val + str(args[x]) + " "
    p_val = p_val[0:-1]
    stacks.push_stack(args[len(args) - 1], p_val)

def DeleteFromStack(args):
    stacks.pop_stack(args[0])

def PushStackSizeOntoStack(args):
    length = stacks.stack_length(args[0])
    stacks.push_stack(args[0], length)

def PrintFromStack(args):
    if not ErrorHandler.has_done_error:
        print(stacks.get_stack_val(args[0])) 

def PrintAsciiFromStack(args):
    if not ErrorHandler.has_done_error:
        print(chr(stacks.get_stack_val_force_type(args[0], int)))

COMMAND_MAP = {
    "c": ClearStack,
    "psh": PushToStack,
    "del": DeleteFromStack,
    "sze": PushStackSizeOntoStack,
    "prt": PrintFromStack,
    "pas": PrintAsciiFromStack
    # if 
    # for
    # fnc
    # cll
}

def RunLine(line):
    command = line.split(" ")

    COMMAND_MAP[command[0]](command[1:])

with open("input.txt", "r", encoding="utf-8") as i:
    lines = i.read().split("\n")

    line_num = 0
    for line in lines:
        line_num = line_num + 1
        if len(line) == 0:
            continue
        ErrorHandler.current_line_num = line_num
        RunLine(line.strip())