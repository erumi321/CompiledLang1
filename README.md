
# General Workings

This language has been intended to look like and act similar to Assembly, but not have to deal with memory addresses (ew). Due to this, it is limited to just the console, but that's ok. It uses a set of commands that are each 3 letters long, and then numbers that tell the command to reference the value off of different stacks (up to 4,294,967,296 [32-bit int] stacks can be used)

  

# Documentation

Syntax <c‍ommand_name> <‍args> (english name)

<input_stack> and <‍target_stack> imply that the command is being given a number that affects that stack

<‍stack_num> implies that the command is being given a stack to read the top value off of

Unless otherwise stated, all stacks are only read and not modified by commands

  

### clr <target_stack> (clear)

Clears all of the values off a stack, making it empty

  

### psh <‍value_1> <‍value_2> ... <target_stack> (push)

Concatenates every arg before the final one into a string and pushes it onto the top of the provided stack

  

### del <target_stack> (delete)

Removes the top value from a stack

  

### sze <target_stack> (size)

Pushes the size of the stack at the current moment onto the top of the stack as an integer

ex. A stack with values ['1', '2', '3'] (with 1 being the top value) would become ['3', '1', '2', '3']

  

### prt <stack_num> (print)

Prints the top value off of the stack and concatenates a line break onto the end, does not change the stack at all

  

### psl <stack_num> (print same line)

Prints the top value off of the stack does NOT end in a line break, does not change the stack at all

  

### mov <input_stack>  <target_stack> (move)

Pops the top value off of the input stack and pushes it on top of the target stack

  

### add <input_stack_1>  <input_stack_2>  <target_stack> (addition)

Adds the top value of input_stack_1 and the top value of input_stack_2 together and pushes the sum on top of target_stack, does not change input_stack_1 or input_stack_2

  

### sub <input_stack_1>  <input_stack_2>  <target_stack> (subtraction)

Subtracts the top value of input_stack_2 from the top value of input_stack_1 together and pushes the difference on top of target_stack, does not change input_stack_1 or input_stack_2

  

### mlt <input_stack_1>  <input_stack_2>  <target_stack> (multiply)

Multiplies the top value of input_stack_1 by the top value of input_stack_2 and pushes the product on top of target_stack, does not change input_stack_1 or input_stack_2

  

### div <input_stack_1>  <input_stack_2>  <target_stack> (divide)

Divides the top value of input_stack_1 by the top value of input_stack_2 and pushes the dividend on top of target_stack, does not change input_stack_1 or input_stack_2

  

### inc <target_stack> (increase)

Adds 1 to the top value of target_stack

  

### dec <target_stack> (decrease)

Subtracts 1 from the top value of target_stack

  

### eql <input_stack_1>  <input_stack_2>  <target_stack> (equal)

Checks if the top value of input_stack_1 is equal to the top value of input_stack_2, if they are, pushes 1 on top of the target_stack, if they are not, pushes 0 on top of the target_stack, does not affect input_stack_1 or input_stack_2

  

### grt <input_stack_1>  <input_stack_2>  <target_stack> (greater then)

Checks if the top value of input_stack_1 is greater than the top value of input_stack_2, if it is, 1 is pushed on top of the target_stack, if it is not, 0 is pushed on top of the target_stack, does not affect input_stack_1 or input_stack_2

  

### lsr <input_stack_1>  <input_stack_2>  <target_stack> (lesser then)

Checks if the top value of input_stack_1 is lesser than the top value of input_stack_2, if it is, 1 is pushed on top of the target_stack, if it is not, 0 is pushed on top of the target_stack, does not affect input_stack_1 or input_stack_2

  

### not <target_stack> (not)

If the top value of target_stack is 0, change it to 1, and vice versa (1 -> 0), if it is neither will throw a runtime error

  

### inp <target_stack> (input)

Creates an input prompt of ">" in the terminal, the resultant input will be pushed as one string on top of target_stack

  

### inp <input_stack>  <target_stack> (input with prompt)

If inp is overloaded with 2 arguments, it will instead offer a prompt of the top value of input_stack and then push the result onto target_stack

  

### nin <target_stack> (number input)

Creates an input prompt of "(Number Input) >" in the terminal, if a non-number value is entered the message <code>Incorrect - this requires a number, please try again:</code> will be displayed and the prompt will be reprinted, repeating until a number is entered

  

### nin <input_stack>  <target_stack> (number input with prompt)

If nin is overloaded with 2 arguments, it will instead offer a prompt of the top value of input_stack with (Number Input) concatenated before it, if a non-number value is entered the message <code>Incorrect - this requires a number, please try again:</code> will be displayed and the prompt will be reprinted, repeating until a number is entered

  

### slp <input_stack> (sleep)

Will read the top value off of input_stack and then wait that many milliseconds

  

### jmp <input_stack>  <target> (jump)

See jump section below

  

### mrk <value> (jump mark)

See jump section below

  

# Jumps
A jump is performed in two parts, a marker is set somewhere in the code with a value, then at another point in the code, a jmp command is set. If the top value of the input_stack for jmp is truthy (not 0, a runtime error will occur if the top value is a string) then the program will jump to the marker with the same <‍value> as the jmp commands <‍target>
ex. - a for loop that prints 3 stars on the same line
```
psh 0 0
psh 3 1
psh * 10
mrk 0
psl 10
inc 0
lsr 0 1 2
jmp 2 0
```

# Special Characters
* <code>$.</code> If the string cosnsits only of $. then it will be substituted for a space ex. (prints <code>a $.a</code>) 
  ```
  psh $. 0
  psh $.a 1
  psh a 2
  psl 2
  psl 0
  psl 1
  ```
  

# Compiling and Running
The compiler and runner run on python.
The compiler takes 2 args input and output, the relative file paths of the locations to read the uncompiled code and write the compiled code to
Input is a .txt file (this is automatically appended)
Output is a .cl1 file (this is automatically appended)
The Runner takes 1 argument input, the relative file path of the compiled code to be run
Input is a .cl1 file (this is automatically appended)
ex. You have program1.txt and want to compile and run it
```
> python -m compiler program1 program1
> python -m runner program1
```
This will create a program1.cl1 file and then run it
