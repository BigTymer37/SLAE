#!/usr/bin/python
# Author: Eric Van Zutphen
# Filename: decrypter.py

from Crypto.Cipher import AES
import base64

def decrypter(encrypted_shellcode):
    PADDING = '{'
    decodeaes = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    secret = 'TMzvovqyJ0QXkjSS1XXwHg=='
    cipher = AES.new(secret)
    decoded = decodeaes(cipher, encrypted_shellcode)
    decoded = ''.join(r'\x{0:02x}'.format(ord(c)) for c in decoded)
    print 'Decrypted Shellcode: ' +decoded

decrypter(b'rqcKstF0c8sB5xa5KKCAhBiOIEAk1PknUBhZ3wUUJuY=')