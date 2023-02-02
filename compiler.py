from binary_helper import *
from stack_manager import StackManager
from error_handler import ErrorHandler

eH = ErrorHandler()

stacks = StackManager(eH)

def ClearStack(args):
    stacks.clear_stack(args[0])

def PushToStack(args):
    stacks.push_stack(args[1], args[0])

def DeleteFromStack(args):
    stacks.pop_stack(args[0])

def PushStackSizeOntoStack(args):
    length = stacks.stack_length(args[0])
    stacks.push_stack(args[0], length)

def PrintFromStack(args):
    print(stacks.get_stack_val(args[0]))

def PrintAsciiFromStack(args):
    print(ord(stacks.get_stack_val(args[0])))

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
    # call
}

def RunLine(line):
    command = line.split(" ")

    COMMAND_MAP[command[0]](command[1:])

i = open("input.txt", "r", encoding="utf-8")

lines = i.read().split("\n")

line_num = 0
for line in lines:
    line_num = line_num + 1
    if len(line) == 0:
        continue
    ErrorHandler.current_line_num = line_num
    RunLine(line.strip())

f = open("output.cl1", "wb")