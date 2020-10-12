"""CPU functionality."""

import sys

#set instructions in binary
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0]*256
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False
        
        while not halted:
            #gets the instruction from the memory using the address in pc 
            instruction = self.ram[self.pc]
            
            #gets the next 2 bytes of data to use in case the instruction needs the next bytes in order to perform the instruction 
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            #checks for different instruction cases 
            if instruction == HLT: #halts the CPU and exits the emulator 
                halted = True
                self.pc += 1
            elif instruction == LDI: #set the value of the register to an integer 
                #operand_a is the register number
                #operand_b is the value to set the register to
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN: #prints numeric value stored in given register 
                #operand_a is the register number
                print(self.reg[operand_a])
                self.pc += 2
            else:
                print(f"Unknown instruction {instruction}")
                sys.exit(1)

    def ram_read(self, address):
        "Accept the address to read and returns the value stored there"
        "Get the address through the pc register"
        #return self.ram[self.mar] 
        return self.ram[address]
    
    def ram_write(self, value):
        "Writes the value to the address passed in"
        "Gets the address through the pc register "
        # self.ram[self.mar] = self.mdr
        self.ram[self.pc] = value