"""CPU functionality."""

import sys

#set instructions in binary
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 #registers on CPU
        self.ram = [0]* 256 #memory
        self.pc = 0 #pointer counter register
        self.ir = 0 #instruction register
        self.mar = 0 #memory address register
        self.mdr = 0 #memory data register

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            #gets program from command line and opens the file
            with open(sys.argv[1]) as program:
                #reads file line by line 
                for self.ir in program:
                    #takes out leading and trailing whitespace
                    self.ir = self.ir.strip()
                    #checks if the line is empty or starts with # and skips the line
                    if self.ir == '' or self.ir[0] == '#':
                        continue
                    try:
                        str_ins = self.ir.split('#')[0].strip()
                        self.ir = int(str_ins, 2)
                    except ValueError:
                        print(f"Invalid number: {self.ir}")
                        sys.exit(1)
                    self.ram[address] = self.ir
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL': #multiples the values in the two registers together and store reult in first
            self.reg[reg_a] *= self.reg[reg_b]
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
            self.ir = self.ram[self.pc]
            
            #gets the next 2 bytes of data to use in case the instruction needs the next bytes in order to perform the instruction
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            #checks for different instruction cases 
            if self.ir == HLT: #halts the CPU and exits the emulator 
                halted = True
            elif self.ir == LDI: #set the value of the register to an integer 
                #operand_a is the register number
                #operand_b is the value to set the register to
                self.reg[operand_a] = operand_b
            elif self.ir == PRN: #prints numeric value stored in given register 
                #operand_a is the register number
                print(self.reg[operand_a])
            elif self.ir == MUL: #sends to ALU to handle self.ir
                self.alu('MUL', operand_a, operand_b)
            else:
                print(f"Unknown self.ir {self.ir}")
                sys.exit(1)
            #gets the first two bits which gives us the number of operands in the self.ir
            instruction_length = ((self.ir & 0b11000000) >> 6) + 1
            self.pc += instruction_length

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