'''
Emulator 
'''
import sys

#symbolic names
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4
PUSH = 5 
POP = 6
CALL = 7
RET = 8

#holds bytes 
#change so that instruction is no longer hardcoded 
#memory starts blank
memory = [0] * 256

#2 byte 3 instructions 
# have more than 1 byte in the whole instruction 

#registers 
#preset names: R0, R1, R2, R3 ... R7
register = [0] * 8 #array of 8 0s
register[7] = 0xf4 #stack pointer 
SP = 7
address = 0

#read program data 
#gets the program name from the command line 
#sys.argv[0] is the name of the program running
#sys.argv[1] is the next word entered into the command line
try:
    with open (sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if line == '' or line[0] == '#':
                continue 
            try:
                str_value = line.split('#')[0]
                #specifies base as base 10 
                value = int(str_value, 10)
            except ValueError:
                print(f"Invalid number: {str_value}")
                sys.exit(1)
            # load into memory at the current address
            memory[address] = value
            address += 1 
except FileNotFoundError:
    print(f"File not found: {sys.argv[1]}")
    sys.exit(2)

#start execution at address 0
#keep track of the address of the currently-executing instruction 
pc = 0 #program counter, pointer to instruction being executed 

#helper function to push on the stack
def push_val(value):
	# Decrement the stack pointer
	register[SP] -= 1
	# Copy the value onto the stack
	top_of_stack_addr = register[SP]
	memory[top_of_stack_addr] = value
    
#helper function to pop off the stadck
def pop_val():
    # Get value from top of stack
    top_of_stack_addr = register[SP]
    value = memory[top_of_stack_addr] # Want to put this in a reg
    # Increment the SP
    register[SP] += 1
    return value
 
halted = False #flag check if program is halted

while not halted:
    instruction = memory[pc]
    if instruction == PRINT_BEEJ : #PRINT_BEEJ
        print("Beej!")
        #move pc to next instruction
        pc += 1
    elif instruction == HALT: #HALT
        halted = True
        pc += 1
    elif instruction == SAVE_REG: #SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3
    elif instruction == PRINT_REG: #PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2
    elif instruction == PUSH:
        #decrement stack pointer
        register[SP] -= 1
        reg_num = memory[pc + 1]
        value = register[reg_num]
        #puts value in given register onto the stack
        memory[register[SP]] = value
        pc += 2
    elif instruction == POP:
        #top of stack addr = register 7
        #pop the value at the top of the stack onto the given register
        reg_num = memory[pc + 1]
        register[reg_num] = memory[register[SP]]
        #increment stack pointer
        register[SP] += 1
        pc += 2
    elif instruction == CALL:
        #address of instruction directly after call is pushed to the stack
        return_addr = pc + 2
        push_val(return_addr)
        #pc is set to the address stored in the given register 
        reg_num = memory[pc + 1]
        subroutine_addr = register[reg_num]
        pc = subroutine_addr
    elif instruction == RET:
        #Pop the value from the top of the stack and store it in the PC.
        return_addr = pop_val()
        pc = return_addr
    else:
        print(f"Unknown instruction {instruction}")
        sys.exit(1)
