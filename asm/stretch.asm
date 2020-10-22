;Test AND, OR, XOR, NOT, SHL, SHR, MOD
;
;Expected Output:
; 2
; 7
; 2
; -3
; 64
; 2
; 1

;MAIN
    LDI R0, 3
    LDI R1, 2
    LDI R2, CheckAnd
    CALL R2
    LDI R2, CheckOr
    CALL R2
    LDI R2, CheckXor
    CALL R2
    LDI R2, CheckNot
    CALL R2
    LDI R2, CheckSHL
    CALL R2
    LDI R2, CheckSHR
    CALL R2
    LDI R2, CheckMod
    CALL R2
    HLT
    

CheckAnd:
    AND R0, R1
    PRN R0
    RET
    

CheckOr:
    LDI R1, 5
    OR R0, R1
    PRN R0
    RET
    
CheckXor:
    XOR R0, R1
    PRN R0
    RET
    
CheckNot:
    NOT R0
    PRN R0
    RET

CheckSHL:
    LDI R0, 2
    SHL R0, R1
    PRN R0
    RET

CheckSHR:
    SHR R0, R1, 
    PRN R0
    RET

CheckMod:
    MOD R1, R0
    PRN R1
    RET