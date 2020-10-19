;Test AND instruction 
; 
;Expected output:
; 2

;MAIN
;    LDI R0, 3
;    LDI R1, 2
;    AND R0, R1
;    PRN R0
;    HLT

;Test JEQ, JGE, JGT, JLE, JLT, JMP, JNE
;
; Expected output:
; 1
; 2
; 2
; 0
; 0
; 2

;MAIN
    LDI R0, 1
    LDI R1, 1
    LDI R2, CheckJEQ
    CALL R2
    LDI R2, CheckJGE
    CALL R2
    LDI R2, CheckJGT
    CALL R2
    LDI R2, CheckJLE
    CALL R2
    LDI R2, CheckJLE2
    CALL R2
    HLT

CheckJEQ:
    PRN R0
    LDI R2, Add
    CMP R0, R1
    JEQ R2
    RET

CheckJGE:
    LDI R2, MUL
    CMP R0, R1
    JGE R2
    RET

CheckJGT:
    LDI R2, And
    CMP R0, R1
    JGT R2
    RET

CheckJLE:
    LDI R2, Dec
    CMP R0, R1
    JLE R2
    RET

CheckJLE2:
    LDI R2, Div
    LDI R0, 4
    LDI R1, 2
    CMP R1, R0
    JLE R2
    RET

Add:
    ADD R0, R1
    PRN R0 
    RET

And:
    AND R0, R1
    PRN R0
    RET

Dec:
    DEC R1
    PRN R1
    RET

Div:
    DIV R0, R1
    PRN R0
    RET

Mul:
    MUL R0, R1
    PRN R0
    RET

