def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symb in plaintext:
        if 'A' <= symb <= 'Z' or 'a' <= symb <= 'z':
            symb_code = ord(symb) + 3
            if ord('Z') < symb_code < ord('a') or symb_code > ord('z'):
                symb_code -= 26
            ciphertext += chr(symb_code)
        else:
            ciphertext += symb
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symb in ciphertext:
        if 'A' <= symb <= 'Z' or 'a' <= symb <= 'z':
            symb_code = ord(symb) - 3
            if ord('Z') < symb_code < ord('a') or symb_code < ord('A'):
                symb_code += 26
            plaintext += chr(symb_code)
        else:
            plaintext += symb

    return plaintext


print(encrypt_caesar('Python3.7'))
print(decrypt_caesar('Sbwkrq3.7'))
