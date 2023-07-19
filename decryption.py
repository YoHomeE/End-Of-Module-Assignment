def decrypt_msg(self, ciphertext):
        """
        Decrypt the given ciphertext using the reverse substitution cipher.

        Args:
            ciphertext (str): The ciphertext to be decrypted.

        Returns:
            str: The decrypted plaintext.
        """
        plaintext = []
        for k in ciphertext:
            v = self.DECRYPTION_DICT.get(k, k)
            plaintext.append(v)
        return ''.join(plaintext)
