"""CPU functionality."""

import sys

#constants
SP = 7 #register 7 is reserved as SP

class CPU:
    """Main CPU class."""

#AABCDDDD 
#01100101 - INC alu
#01000101 - PUSH
#AA - number operands
#B - alu op
#C - sets pc
#DDDD - instruction identifier

    def __init__(self):
        """Construct a new CPU."""
        #set instructions in binary using instruction idenifier
        self.opcodes = {
            'ADD' : 0b0000,
            'AND' : 0b1000,
            'CMP' : 0b0111,
            'DEC' : 0b0110,
            'DIV' : 0b0011, 
            'HLT' : 0b0001,
            'INC' : 0b0101,
            'LDI' : 0b0010,
            'MOD' : 0b0100,
            'MUL' : 0b0010,
            'NOT' : 0b1001,
            'OR'  : 0b1010,
            'POP' : 0b0110,
            'PRN' : 0b0111,
            'PUSH': 0b0101,
            'SHL' : 0b1100,
            'SHR' : 0b1101,
            'SUB' : 0b0001,
            'XOR' : 0b1011
        }
        self.reg = [0] * 8 #registers on CPU
        self.reg[SP] = 0xF4 #pointer to the top of the stack
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
        self.branchtable[self.opcodes['DIV']] = self.handle_div
        self.branchtable[self.opcodes['HLT']] = self.handle_hlt
        self.branchtable[self.opcodes['INC']] = self.handle_inc
        self.branchtable[self.opcodes['LDI']] = self.handle_ldi
        self.branchtable[self.opcodes['MOD']] = self.handle_mod
        self.branchtable[self.opcodes['MUL']] = self.handle_mul
        self.branchtable[self.opcodes['NOT']] = self.handle_not
        self.branchtable[self.opcodes['OR']]  = self.handle_or
        self.branchtable[self.opcodes['POP']] = self.handle_pop
        self.branchtable[self.opcodes['PRN']] = self.handle_prn
        self.branchtable[self.opcodes['SHL']] = self.handle_shl
        self.branchtable[self.opcodes['SHR']] = self.handle_shr
        self.branchtable[self.opcodes['SUB']] = self.handle_sub 
        self.branchtable[self.opcodes['XOR']] = self.handle_xor 
        

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
        
        #checks if op is div or mod to make sure you aren't dividing by 0
        if op == 'DIV' or op == 'MOD':
            #sends an error message in the value in second register is 0 and halts the emulator
            if self.reg[reg_b] == 0:
                print("You can't divide by zero. Stopping program")
                self.handle_hlt()
            self.branchtable[self.opcodes[op]](reg_a, reg_b)
        
        #check if it's one of the operations with only 1 register needed
        if op == 'INC' or op =='DEC' or op == 'NOT':
            self.branchtable[self.opcodes[op]](reg_a)
        
        try:
            self.branchtable[self.opcodes[op]](reg_a, reg_b)
        except:
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
        
         

        
        while not self.halted:
            #gets the instruction from the memory using the address in pc 
            self.ir = self.ram[self.pc]

            #get number of operands from instruction 
            #first two bits 
             #use and mask to clear all other bits and get the first two bits 
            #shift so that left with just the num of operands bits                
            num_operands = (self.ir & 0b11000000) >> 6
            #get if instruction is performed by alu
            go_alu = (self.ir & 0b00100000) >> 5
            #get if instruction sets pc
            set_pc = (self.ir & 0b00010000) >> 6 + 1
            #get instruction identifier
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
                    
                self.branchtable[ins](operand_a, operand_b)
                
            elif num_operands == 1:
                operand = self.ram_read(self.pc + 1)
                
                if bool(go_alu):
                    op = ''
                    if ins == self.opcodes['DEC']:
                        op = 'DEC'
                    if ins == self.opcodes['INC']:
                        op = 'INC'
                        
                    self.alu(op, operand)
                
                #check if instruction identifier is push since the instruction identifier for INC and PUSh is the same
                if ins == self.opcodes['PUSH']:
                    self.branchtable[self.opcodes['PUSH']](operand)
                
                self.branchtable[ins](operand)
                
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
        
    #divides the value in the first register by the value in the second register and stores the result in the first register
    def handle_div(self, reg_a, reg_b):
        self.reg[reg_a] /= self.reg[reg_b]
            
    #halts the CPU and exits the emulator 
    def handle_hlt(self):
        self.halted = True
        
    #increments the value in the given register by 1
    def handle_inc(self, reg_a):
        self.reg[reg_a] += 1
        
    #set the value of the register to an integer 
    def handle_ldi(self, reg_a, operand_b):
        #operand_a is the register number
        #operand_b is the value to set the register to
        self.reg[reg_a] = operand_b

    #divides the value in the first register by the value in the second register and stores the remainder in the first register
    def handle_mod(self, reg_a, reg_b):
        self.reg[reg_a] %= self.reg[reg_b]
        
    #multiples the values in the two registers together and stores the result in the first register
    def handle_mul(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        
    #perform a bitwise NOT on the value in the given register and store the result in the same register
    def handle_not(self, reg_a):
        self.reg[reg_a] = ~self.reg[reg_a]
        
    #preforms a bitwise OR between the values in two registers and stores the result in the first register
    def handle_or(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        
    #pops the value at the top of the stack into the given register 
    def handle_pop(self, reg_a):
        #copy value from address pointed to by SP to the given register
        reg_a = self.reg[SP]
        #increment SP
        self.reg[SP] += 1
        
    #pushes the value in the given register onto the stack
    def handle_push(self, reg_a):
        #decrements SP by 1
        self.reg[SP] -= 1
        #copy value in given register to address pointed to by SP
        self.reg[reg_a] = self.ram[self.reg[SP]]

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
        
    #shifts the value in the first register by the number of bits specified in the second register to the left 
    def handle_shl(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        
    #shifts the value in the first register by the of bits specified in the second register to the right
    def handle_shr(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b] 
        
    #subtracts the value in the first register by the value in the second register and stores the result in the first register
    def handle_sub(self, reg_a, reg_b):
        self.reg[reg_a] -= self.reg[reg_b]
        
    #performs a bitwise XOR between the values in the two registers and stores the result in the first register 
    def handle_xor(self, reg_a, reg_b): 
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b] 