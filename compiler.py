from binary_helper import *

stacks = {}

def ClearStack(args):
    stacks[args[0]] = {}
    print("clear")

def PushToStack(args):
    print(args)
    stacks[args[0]].insert(0, args[1])
    print("push")

def DeleteFromStack(args):
    stacks[args[0]].pop(args[1])
    print("delete")

def PushStackSizeOntoStack(args):
    stacks[args[0]].insert(0, len(stacks[args[0]]))
    print("push")

def PrintFromStack(args):
    print(stacks[args[0]])

def PrintAsciiFromStack(args):
    print(ord(stacks[args[0]]))

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
    
    print(command[1:])

    COMMAND_MAP[command[0]](command[1:])

i = open("input.txt", "r", encoding="utf-8")

lines = i.read().split("\n")

for line in lines:
    if len(line) == 0:
        continue
    RunLine(line.strip())

f = open("output.cl1", "wb")