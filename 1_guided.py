'''
Emulator 
'''
import sys

#holds bytes 
memory = [
    1, #PRINT_BEEJ
    3, #SAVE_REG R1, 37 --> r[1] = 37
    1, #register number
    37, #value 
    4, #PRINT_REG R1 --> print(r[1])
    1, #PRINT_BEEJ
    2  #HALT
]

#registers 
#preset names: R0, R1, R2, R3 ... R7
register = [0] * 8 #array of 8 0s

#start execution at address 0
#keep track of the address of the currently-executing instruction 
pc = 0 #program counter, pointer to instruction being executed 

halted = False #flag check if program is halted

while not halted:
    instruction = memory[pc]
    if instruction == 1 : #PRINT_BEEJ
        print("Beej!")
        #move pc to next instruction
        pc += 1
    elif instruction == 2: #HALT
        halted = True
        pc += 1
    elif instruction == 3: #SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3
    elif instruction == 4: #PRINT_REG
        print(register)
        pc += 1
    else:
        print(f"Unknown instruction {instruction}")
        sys.exit(1)