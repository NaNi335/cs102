def encrypt_caesar(plaintext: str) -> str:
    """
    This function encrypts a message using a Caesar cipher.

    :param plaintext: word that must be encrypted
    :return: encrypted word
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


def decrypt_caesar(ciphertext: str) -> str:
    """
    This function decrypts an encrypted message using a Caesar cipher.

    :param ciphertext: word that must be decrypted
    :return: decrypted word
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
