# Number Bases

- Base 2 - binary "bits"
- Base 8 - octal
- Base 10 - decimal
- Base 16 - hexadecimal ("hex")
- Base 64 - "base 64"

- Base 10 - numbering system we learn in school. Not convenient for computers. 
    - Digits 0-9
    - Shows number based on the power of 10
        ex. 12 --> one 10 and two 1s ... 1 * 10 + 2 * 1 = 12
        - 1s place = 10^0
        - 10s place = 10^1
        - 100s = 10^2
        - 1000s = 10^3
        - etc. 

- Base 2 - numbering system with 0s and 1s
    - Digits: 0-1
    - Counting 
        - 0 (1s place) --> 0
        - 1 (1s place) --> 1
        - 10 (2s place) --> 2
        - 11 (2s place) --> 3
        - 100 (4s place) --> 4 * 1 + 2 * 0 + 1 * 0 --> 4
        - 101 --> 4 * 1 + 2 * 0 + 1 * 1 --> 5
        - 110 --> 6 
        - 111 --> 7
        - 1000 --> 8
    - 1s = 2^0
    - 2s = 2^1
    - 4s = 2^2
    - 8s = 2^3
    - 16s = 2^4
    - etc. 
    - 1 place is a bit
    - 4 bits == 1 nybble
    - 8 bits == 1 byte 

- Base 16 - hexadecimal "hex"
    - Digits: 0-9, A-F
    - Counting
        - 0
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - A --> 10
        - B --> 11
        - C --> 12
        - D --> 13
        - E --> 14
        - F --> 15
    - 1F --> 16
# Convert Hex to Binary
- 1 hex digit === 4 binary digits
- 0x87 --> 0b ???? ???? --> 0b 1000 0111 --> 0b10000111
- Convert the Binary to Decimal
    - 0b10000111 --> 270

- 0x0C --> 0b 0000 1100 --> 0b00001100 --> 0b1100

- 0xFF --. 0b 1111 1111 --> 0b11111111

# Python base number
- Python is in decimal by default  
- Let python know you want the number in binary 
     - 0b110
- Prefixes 
    - 0b --> binary
    - 0x --> hex
    - 0o --> octal 

# Bitewise Operators
- Boolean
    - and &&
    - or ||
    - not !
    - truth table

A | B | A and B | A or B | 
----|----|----- | ---- | 
F | F | F | F | 
F | T | F | T
T | F | F | T
T | T | T  | T

- Bitwise
    - and &
    - or |
    - not ~
    -truth table

A | B | A & B | A or B
----|----|----|----
0 | 0 | 0 | 0 
0 | 1 | 0 | 1
1 | 0 | 0 | 1
1 | 1 | 1 | 1

A | not A (~A)
----|----
0 | 1 
1 | 0 
 
    
```  0b1010101
   & 0b1111000
   ------------
     0b1010000
```

# Emulator program
- Memory 
    - holds bytes
    - big array of bytes 
    - to get or set data in memory, you need the index in the array 
    - Index into memory array === Address === Location === Pointer 
- Instructions have to be made up of numbers 
    - opcode == instruction byte
    - operands == arguments to the instruction
- Variables are called 'registers'
    - there are a fixed number 
    - they have preset names 
    - registers can each hold a single byte 

