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
; 2
; 4

;MAIN
    LDI R0, 1
    LDI R1, 1
    LDI R2, CheckJEQ
    JEQ R2
    LDI R2, CheckJGE
    JGE R2 

CheckJEQ:
    ADD R0, R1
    PRN R0

CheckJGE:
    LDI R1, 2
    MUL R0, R1
    PRN R0
    HLT