;Test AND, OR, XOR, NOT, SHL, SHR, MOD
;
;Expected Output:
; 2
; 7

;MAIN
    LDI R0, 3
    LDI R1, 2
    LDI R2, CheckAnd
    CALL R2
    

CheckAnd:
    AND R0, R1
    PRN R0
    

CheckOr:
    LDI R1, 5
    OR R0, R1
    PRN R0
    HLT