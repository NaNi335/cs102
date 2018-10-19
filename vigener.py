def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for index, symb in enumerate(plaintext):
        if 'a' <= symb <= 'z' or 'A' <= symb <= 'Z':
            move = ord(keyword[index % len(keyword)])
            if 'a' <= symb <= 'z':
                move -= ord('a')
            else:
                move -= ord('A')
            nindex = ord(symb) + move
            if 'a' <= symb <= 'z' and nindex > ord('z'):
                nindex -= 26
            elif 'A' <= symb <= 'Z' and nindex > ord('Z'):
                nindex -= 26
            ciphertext += chr(nindex)
        else:
            ciphertext += symb
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for num, symb in enumerate(ciphertext):
        if 'A' <= symb <= 'Z' or 'a' <= symb <= 'z':
            move = ord(keyword[num % len(keyword)])
            move -= ord('a') if 'z' >= symb >= 'a' else ord('A')
            nindex = ord(symb) - move
            if 'a' <= symb <= 'z' and nindex < ord('a'):
                nindex += 26
            elif 'A' <= symb <= 'Z' and nindex < ord('A'):
                nindex += 26
            plaintext += chr(nindex)
        else:
            plaintext += symb
    return plaintext


print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))
print(decrypt_vigenere('LXFOPVEFRNHR', 'LEMON'))
