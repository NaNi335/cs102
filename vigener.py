def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    This function encrypts a message using a Vigenere cipher.

    :param plaintext: word that must be encrypted
    :param keyword: key which will be used for encryption
    :return: encrypted word
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


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    This function decrypts an encrypted message using a Vigenere cipher.

    :param ciphertext: word that must be decrypted
    :param keyword:  key which will be used for decryption
    :return: decrypted word
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
