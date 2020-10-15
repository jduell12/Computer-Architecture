"""CPU functionality."""

import sys

#constants
IM = 5 #register R5 is reserved as IM
IS = 6 #register R6 is reserved as IS
SP = 7 #register R7 is reserved as SP

class CPU:
    """Main CPU class."""

#Instruction byte: AABCDDDD 
#AA - number operands
#B - alu op
#C - sets pc
#DDDD - instruction identifier

    def __init__(self):
        """Construct a new CPU."""
        #set instructions in binary using instruction idenifier
        self.opcodes = {
            'ADD' : 0b10100000,
            'AND' : 0b10101000,
            'CALL': 0b01010000,
            'CMP' : 0b10100111,
            'DEC' : 0b01100110,
            'DIV' : 0b10100011, 
            'HLT' : 0b00000001,
            'INC' : 0b01100101,
            'INT' : 0b01010010,
            'LDI' : 0b10000010,
            'MOD' : 0b10100100,
            'MUL' : 0b10100010,
            'NOT' : 0b01101001,
            'NOP' : 0b00000000,
            'OR'  : 0b10101010,
            'POP' : 0b01000110,
            'PRA' : 0b01001000,
            'PRN' : 0b01000111,
            'PUSH': 0b01000101,
            'RET' : 0b00010001,
            'SHL' : 0b10101100,
            'SHR' : 0b10101101,
            'ST'  : 0b10000100, 
            'SUB' : 0b10100001,
            'XOR' : 0b10101011
        }
        self.lookUpOpcodes = dict(map(reversed, self.opcodes.items()))
        self.reg = [0] * 8 #registers on CPU
        self.reg[IM] = 0 #interrupt mask (IM)
        self.reg[IS] = 0 #interrupt status (IS)
        self.reg[SP] = 0xF4 #pointer to the top of the stack, SP
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
        self.branchtable = {
            self.opcodes['ADD']: self.handle_add,
            self.opcodes['AND']: self.handle_and,
            self.opcodes['CALL']: self.handle_call, 
            self.opcodes['CMP']: self.handle_cmp,
            self.opcodes['DEC']: self.handle_dec,
            self.opcodes['DIV']: self.handle_div,
            self.opcodes['HLT']: self.handle_hlt,
            self.opcodes['INC']: self.handle_inc,
            self.opcodes['INT']: self.handle_int,
            self.opcodes['LDI']: self.handle_ldi,
            self.opcodes['MOD']: self.handle_mod,
            self.opcodes['MUL']: self.handle_mul,
            self.opcodes['NOT']: self.handle_not,
            self.opcodes['NOP']: self.handle_nop,
            self.opcodes['OR']: self.handle_or,
            self.opcodes['POP']: self.handle_pop,
            self.opcodes['PUSH']: self.handle_push,
            self.opcodes['PRA']: self.handle_pra,
            self.opcodes['PRN']: self.handle_prn,
            self.opcodes['RET']: self.handle_ret,
            self.opcodes['SHL']: self.handle_shl,
            self.opcodes['SHR']: self.handle_shr,
            self.opcodes['ST'] : self.handle_st,
            self.opcodes['SUB']: self.handle_sub,
            self.opcodes['XOR']: self.handle_xor 
        }
        

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
            set_pc = (self.ir & 0b00010000) >> 4 
            #get instruction identifier
            ins = self.ir
            
            #gets as many operands as the instruction byte indicates 
            if num_operands == 2:
                #gets the next 2 bytes of data to use in case the instruction needs the next bytes in order to perform the instruction
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                
                if bool(go_alu):
                    op = self.lookUpOpcodes[ins]
                    self.alu(op, operand_a, operand_b)
                else:    
                    self.branchtable[ins](operand_a, operand_b)
                
            elif num_operands == 1:
                operand = self.ram_read(self.pc + 1)
                
                if bool(go_alu):
                    op = op = self.lookUpOpcodes[ins]    
                    self.alu(op, operand)

                self.branchtable[ins](operand)
            else:
                self.branchtable[ins]()

            #gets the first two bits which gives us the number of operands in the self.ir
            if not bool(set_pc):
                self.pc += num_operands + 1
            

    ############## functions for each instruction in spec ####################            

    #adds the values in the two registers together and stores the result in the first register        
    def handle_add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]

    #performs bitwise and on the values in the two registers and stores the result in the first register
    def handle_and(self, reg_a, reg_b):
        self.reg[reg_a] &= self.reg[reg_b]
        
    #calls a subroutine at the address stored in the register 
    def handle_call(self, reg_a):
        return_addr = self.pc + 2
        self.push_val(return_addr)
        #pc is set to address stored in given register
        subroutine_addr = self.reg[reg_a]
        self.pc = subroutine_addr
        
        
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
        
    #issues the interrupt number that is stored in the given register    
    def handle_int(self, reg_a):
        self.reg[IS] = self.reg(reg_a)
        
    #returns from the interrupt handler 
    def handle_iret(self):
        #registers R6-R0 are pooped off the stack in that order
        for i in range(6, -1, -1):
            self.reg[i] = self.pop_val()
        #fl register is popped off the stack
        self.fl = self.pop_val()
        self.pc = self.pop_val()
        #re-enables interrupts
        self.reg[IS] = 0
        
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
        
    #do nothing 
    def handle_nop(self):
        return
        
    #perform a bitwise NOT on the value in the given register and store the result in the same register
    def handle_not(self, reg_a):
        self.reg[reg_a] = ~self.reg[reg_a]
        
    #preforms a bitwise OR between the values in two registers and stores the result in the first register
    def handle_or(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        
    #pops the value at the top of the stack into the given register 
    def handle_pop(self, reg_a):
        #copy value from address pointed to by SP to the given register
        self.reg[reg_a] = self.ram[self.reg[SP]]
        #increment SP
        self.reg[SP] += 1
        
    #print alpha character value stored in the given registiver 
    def handle_pra(self, reg_a):
        #reg_a is the register number 
        print(chr(self.reg[reg_a]))

    #prints numeric value stored in given register 
    def handle_prn(self, reg_a):
        #reg_a is the register number
         print(self.reg[reg_a])
         
    #pushes the value in the given register onto the stack
    def handle_push(self, reg_a):
        #decrements SP by 1
        self.reg[SP] -= 1 
        #copy value in given register to address pointed to by SP
        self.ram[self.reg[SP]] = self.reg[reg_a]
         
    #returns from the subroutine
    def handle_ret(self):
        #pop value from top of stack
        return_addr = self.pop_val()
        self.pc = return_addr
        
        
    #shifts the value in the first register by the number of bits specified in the second register to the left 
    def handle_shl(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        
    #shifts the value in the first register by the of bits specified in the second register to the right
    def handle_shr(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b] 
        
    #store value in second register in the address stored in first register
    def handle_st(self, reg_a, reg_b):
        value = self.reg[reg_b]
        address = self.reg[reg_a]
        self.ram[address] = value
        
    #subtracts the value in the first register by the value in the second register and stores the result in the first register
    def handle_sub(self, reg_a, reg_b):
        self.reg[reg_a] -= self.reg[reg_b]
        
    #performs a bitwise XOR between the values in the two registers and stores the result in the first register 
    def handle_xor(self, reg_a, reg_b): 
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b] 
        
        
    ######### helper functions #########################
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
        
    def push_val(self, value):
        #decrement the stack pointer
        self.reg[SP] -= 1
        #copy value onto the stack
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = value
        
    def pop_val(self):
        #get value from top of stack
        top_of_stack_addr = self.reg[SP]
        value = self.ram[top_of_stack_addr]
        #increment SP
        self.reg[SP] += 1
        return value 