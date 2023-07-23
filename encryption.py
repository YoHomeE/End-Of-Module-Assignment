import string

CHAR_SET = string.printable[:-5]
SUBSTITUTION_CHARS = CHAR_SET[-3:] + CHAR_SET[:-3]

ENCRYPTION_DICT = {}
DECRYPTION_DICT = {}

for i, k in enumerate(CHAR_SET):
    v = SUBSTITUTION_CHARS[i]
    ENCRYPTION_DICT[k] = v
    DECRYPTION_DICT[v] = k


def encrypt_msg(plaintext):
    """
    Encrypt the given plaintext using a simple substitution cipher.

    Args:
        plaintext (str): The plaintext to be encrypted.

    Returns:
        str: The encrypted ciphertext.
    """
    ciphertext = []
    for k in plaintext:
        v = ENCRYPTION_DICT.get(k, k)
        ciphertext.append(v)
    return "".join(ciphertext)


def decrypt_msg(ciphertext):
    """
    Decrypt the given ciphertext using the reverse substitution cipher.

    Args:
        ciphertext (str): The ciphertext to be decrypted.

    Returns:
        str: The decrypted plaintext.
    """
    plaintext = []
    for k in ciphertext:
        v = DECRYPTION_DICT.get(k, k)
        plaintext.append(v)
    return "".join(plaintext)


def encrypt_list_of_dicts(plaintext):
    """
    Encrypt the given plaintext using a simple substitution cipher.

    Args:
        plaintext (str): The plaintext to be encrypted.

    Returns:
        str: The encrypted ciphertext.
    """

    encrypted_output = []
    for member in plaintext:
        encrypted_text = {}
        for key, value in member.items():
            encrypted_key = encrypt_msg(key)
            encrypted_value = encrypt_msg(value)
            encrypted_text[encrypted_key] = encrypted_value
        encrypted_output.append(encrypted_text)
        print("Encrypted dictionary:")
        print(encrypted_output)
        return encrypted_output


def decrypt_list_of_dicts(ciphertext):
    """
    Decrypt the given ciphertext using the reverse substitution cipher.

    Args:
        ciphertext (str): The ciphertext to be decrypted.

    Returns:
        str: The decrypted plaintext.
    """

    decrypted_output = []
    for member in ciphertext:
        decrypted_text = {}
        for key, value in member.items():
            decrypted_key = decrypt_msg(key)
            decrypted_value = decrypt_msg(value)
            decrypted_text[decrypted_key] = decrypted_value
        decrypted_output.append(decrypted_text)
        print("Decrypted dictionary:")
        print(decrypted_output)
        return decrypted_output
