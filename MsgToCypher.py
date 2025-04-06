#!/usr/bin/env python

# encrypt and decrypt with AES and IV
#
# Encrypt :
#  
# python ./MsgToCypher.py test
# python ./MsgToCypher.py enc test 3S8C/nPgfAEu0HAxsZQmz3bWfowPIjtbHAv038b6Nvk= K3kFByTQGpDPnyUIdKLFrg==
#
# Decrypt : 
#
# python ./MsgToCypher.py dec Y6vbUV4JWmkJwgJluZwQEw== 3S8C/nPgfAEu0HAxsZQmz3bWfowPIjtbHAv038b6Nvk= K3kFByTQGpDPnyUIdKLFrg==
#
# /!\ Be aware that IVs should not be used twice ! 
#


import base64
import secrets
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


# Chiffrer une chaîne de caractères
def chiffre_message(cle, iv, message):

    padder = padding.PKCS7(128).padder()
    message = message.encode()
    message = padder.update(message) + padder.finalize()
    cipher = Cipher(algorithms.AES(cle), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

# Déchiffrer un message
def dechiffre_message(cle, iv, ct):
    
    cipher = Cipher(algorithms.AES(cle), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    message = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(message) + unpadder.finalize()
    return message.decode()



if __name__ == "__main__":

    if len(sys.argv) != 2 and len(sys.argv) != 5:
        print("Usage to encrypt with random key: <script> <msg>")
        print("Usage to encrypt: <script> enc <msg> <key_base64> <iv_base64>")
        print("Usage to decrypt: <script> dec <cipher_base64> <key_base64> <iv_base64>")
        sys.exit(0)

    if len(sys.argv) == 2:
        m = sys.argv[1]
        k = secrets.token_bytes(32)  # génération d'une clé AES
        i = secrets.token_bytes(16)  # génération d'IVs
        c = chiffre_message(k, i, m)
        print("key:", base64.b64encode(k).decode())
        print("iv:", base64.b64encode(i).decode())
        print("cipher:", base64.b64encode(c).decode())

    if len(sys.argv) == 5:

        if sys.argv[1] == 'enc':
            m = sys.argv[2]
            k = base64.b64decode(sys.argv[3])
            i = base64.b64decode(sys.argv[4])
            c = chiffre_message(k, i, m)
            print("key:", base64.b64encode(k).decode())
            print("iv:", base64.b64encode(i).decode())
            print("cipher:", base64.b64encode(c).decode())

        if sys.argv[1] == 'dec':
            c = base64.b64decode(sys.argv[2])
            k = base64.b64decode(sys.argv[3])
            i = base64.b64decode(sys.argv[4])
            m = dechiffre_message(k, i, c)
            print("message:", m)
