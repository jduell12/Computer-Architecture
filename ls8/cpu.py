"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #set instructions in binary using instruction idenifier
        self.opcodes = {
            'ADD' : 0b0000,
            'AND' : 0b1000,
            'CMP' : 0b0111,
            'DEC' : 0b0110,
            'HLT' : 0b0001,
            'INC' : 0b0101,
            'LDI' : 0b0010,
            'MUL' : 0b0010,
            'PRN' : 0b0111,
        }
        self.reg = [0] * 8 #registers on CPU
        self.ram = [0] * 256 #memory
        self.pc = 0 #pointer counter register
        self.ir = 0 #instruction register
        self.mar = 0 #memory address register
        self.mdr = 0 #memory data
        #flag register to hold current flags status
        #made of 8 bits and if a particular bit is set the flag is "true"
        # FL bits: 00000LGE
        # L -> less-than, reg_a < reg_b
        # G -> greater-than, reg_a > reg_b
        # E -> equal, reg_a == reg_b
        self.fl = 0b000000 
        self.halted = False #flag to check if running
        #sets up branch table to be able to look up instructions quickly
        self.branchtable = {}
        self.branchtable[self.opcodes['ADD']] = self.handle_add
        self.branchtable[self.opcodes['AND']] = self.handle_and
        self.branchtable[self.opcodes['CMP']] = self.handle_cmp
        self.branchtable[self.opcodes['DEC']] = self.handle_dec
        self.branchtable[self.opcodes['HLT']] = self.handle_hlt
        self.branchtable[self.opcodes['INC']] = self.handle_inc
        self.branchtable[self.opcodes['LDI']] = self.handle_ldi
        self.branchtable[self.opcodes['MUL']] = self.handle_mul
        self.branchtable[self.opcodes['PRN']] = self.handle_prn
        

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
        
        if op == 'DIV' or op == 'MOD':
            #sends an error message in the value in second register is 0 and halts the emulator
            if self.reg[reg_b] == 0:
                print("You can't divide by zero. Stopping program")
                self.handle_hlt()
            self.branchtable[op](reg_a, reg_b)
        
        if op == 'INC' or 'DEC':
            self.branchtable[op](reg_a)
        
        self.branchtable[op](reg_a, reg_b)
        
        
        if op == "ADD":
            #adds the values in the two registers together and stores the result in the first register
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL': 
            #multiples the values in the two registers together and stores the result in the first register
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':

            #divides the value in the first register by the value in the second register and stores the result in the first register
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 'MOD':
            #sends an error message in the value in second register is 0 and halts the emulator
            if self.reg[reg_b] == 0:
                print("You can't divide by zero. Stopping program")
                self.handle_hlt()
            #divides the value in the first register by the value in the second register and stores the remainder in the first register
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 'INC':
            #increments the value in the given register by 1
            self.reg[reg_a] += 1
        elif op == 'DEC':
            #subtracts 1 from the value in the given register
            self.reg[reg_a] -= 1
        elif op == 'AND':
            #performs bitwise and on the values in the two registers and stores the result in the first register
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'CMP':
            #compares the values in the two registers and sets the FL register based on the comparison
            if self.reg[reg_a] > self.reg[reg_b]:
                #set the G flag to 1 while setting E and L flags to 0 using bitwise AND
                self.fl = self.fl & 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                #set L flag to 1 while setting E and G flag to 0 using bitwise AND
                self.fl = self.fl & 0b00000100
            else:
                #set E flag 
                self.fl = self.fl | 0b00000001
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
        
        self.ir = self.ram[self.pc]
        
        #get number of operands from instruction 
        #first two bits 
        #use and mask to clear all other bits and get the first two bits 
        #shift so that left with just the num of operands bits 

        
        while not self.halted:
            #gets the instruction from the memory using the address in pc 
            self.ir = self.ram[self.pc]
            
            num_operands = (self.ir & 0b11000000) >> 6
            go_alu = (self.ir & 0b00100000) >> 5
            set_pc = (self.ir & 0b00010000) >> 6 + 1
            ins = (self.ir & 0b00001111)
            
            #gets as many operands as the instruction byte indicates 
            if num_operands == 2:
                #gets the next 2 bytes of data to use in case the instruction needs the next bytes in order to perform the instruction
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                
                if bool(go_alu):
                    op = ""
                    if ins == self.opcodes['MUL']:
                        op = 'MUL'
                        
                    self.alu(op, operand_a, operand_b)
                    
                elif ins == self.opcodes['LDI']:
                    self.handle_ldi(operand_a, operand_b)
                
            elif num_operands == 1:
                operand = self.ram_read(self.pc + 1)
                
                if bool(go_alu):
                    op = ''
                    if ins == self.opcodes['DEC']:
                        op = 'DEC'
                        
                    self.alu(op, operand)
                
                if ins == self.opcodes['PRN']:
                    self.handle_prn(operand)
                
            if ins == self.opcodes['HLT']:
                self.handle_hlt()

            #gets the first two bits which gives us the number of operands in the self.ir
            self.pc += num_operands + 1
            
    #adds the values in the two registers together and stores the result in the first register        
    def handle_add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]

    #performs bitwise and on the values in the two registers and stores the result in the first register
    def handle_and(self, reg_a, reg_b):
        self.reg[reg_a] &= self.reg[reg_b]
        
    #compares the values in the two registers and sets the FL register based on the comparison
    def handle_cmp(self, reg_a, reg_b):
        if self.reg[reg_a] > self.reg[reg_b]:
            #set the G flag to 1 while setting E and L flags to 0 using bitwise AND
            self.fl = self.fl & 0b00000010
        elif self.reg[reg_a] < self.reg[reg_b]:
            #set L flag to 1 while setting E and G flag to 0 using bitwise AND
            self.fl = self.fl & 0b00000100
        else:
            #set E flag 
            self.fl = self.fl | 0b00000001
            
    #subtracts 1 from the value in the given register
    def handle_dec(self, reg_a):
        self.reg[reg_a] -= 1
            
    #halts the CPU and exits the emulator 
    def handle_hlt(self):
        self.halted = True
        
    #set the value of the register to an integer 
    def handle_ldi(self, reg_a, operand_b):
        #operand_a is the register number
        #operand_b is the value to set the register to
        self.reg[reg_a] = operand_b

    #prints numeric value stored in given register 
    def handle_prn(self, reg_a):
        #reg_a is the register number
         print(self.reg[reg_a])
        
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