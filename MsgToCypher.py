#!/usr/bin/env python

# encrypt and decrypt with AES and IV
#
# Encrypt :
#  
# python ./MsgToCypher.py test
# python ./MsgToCypher.py enc test 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8
#
# Decrypt : 
#
# python ./MsgToCypher.py dec EFAADCF7EA0A786EF7B4EF7504605970 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8
#
# /!\ Be aware that IVs should not be used twice ! 
#

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
        print("Usage to encrypt: <script> enc <msg> <key_hex> <iv_hex>")
        print("Usage to decrypt: <script> dec <cipher_hex> <key_hex> <iv_hex>")
        sys.exit(0)

    if len(sys.argv) == 2:
        m = sys.argv[1]
        k = secrets.token_bytes(32)  # génération d'une clé AES
        i = secrets.token_bytes(16)  # génération d'IVs
        c = chiffre_message(k, i, m)
        print("key:", k.hex().upper())
        print("iv:", i.hex().upper())
        print("cipherText:", c.hex().upper())
        [print("next iv :", secrets.token_bytes(16).hex().upper()) for i in range(4)]

    if len(sys.argv) == 5:
        if sys.argv[1] == 'enc':
            m = sys.argv[2]
            k = bytes.fromhex(sys.argv[3])
            i = bytes.fromhex(sys.argv[4])
            c = chiffre_message(k, i, m)
            print("key:", k.hex().upper())
            print("iv:", i.hex().upper())
            print("cipherText:", c.hex().upper())

        if sys.argv[1] == 'dec':
            c = bytes.fromhex(sys.argv[2])
            k = bytes.fromhex(sys.argv[3])
            i = bytes.fromhex(sys.argv[4])
            m = dechiffre_message(k, i, c)
            print("message:", m)
