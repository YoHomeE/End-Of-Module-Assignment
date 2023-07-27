import unittest
from encryption import encrypt_list_of_dicts, decrypt_list_of_dicts
from testdata import dict1, dict2, dict3, dict4, emptydict

class TestSubstitutionCipher(unittest.TestCase):
    """Test cases for the Substitution Cipher encryption and decryption functions."""

    def test_encrypt_list_of_dicts(self):
        """
        Test encryption for each dictionary in the test data.

        This test case encrypts each dictionary in the test data using the
        encrypt_list_of_dicts function and checks if the encrypted dictionaries
        are different from the original ones.
        Note this will cause an error on the empty dictionary as it wont change
        """
        for member in [dict1, dict2, dict3, dict4, emptydict]:
            encrypted_dicts = encrypt_list_of_dicts(member)
            self.assertNotEqual(encrypted_dicts, member)  # Encrypted dictionaries should be different from original
            
    def test_decrypt_list_of_dicts(self):
        """
        Test decryption for each dictionary in the test data.

        This test case encrypts each dictionary in the test data using the
        encrypt_list_of_dicts function, then decrypts the encrypted dictionaries
        using the decrypt_list_of_dicts function, and finally checks if the
        decrypted dictionaries are the same as the original ones.
        """
        for member in [dict1, dict2, dict3, dict4, emptydict]:
            encrypted_dicts = encrypt_list_of_dicts(member)
            decrypted_dicts = decrypt_list_of_dicts(encrypted_dicts)
            self.assertEqual(decrypted_dicts, member)  # Decrypted dictionaries should be the same as original

if __name__ == '__main__':
    unittest.main()

