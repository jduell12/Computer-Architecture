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

;Test JEQ, JGE 
;
; Expected output:
; 1
; 2
; 2

;MAIN
    LDI R0, 1
    LDI R1, 1
    LDI R2, CheckJEQ
    CALL R2
    LDI R2, CheckJGE
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

Add:
    ADD R0, R1
    PRN R0 
    RET

Mul:
    MUL R0, R1
    PRN R0
    RET