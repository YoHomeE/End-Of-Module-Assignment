import unittest
from unittest.mock import patch
from client import Client

class TestSaveFile(unittest.TestCase):
    """Test cases for the Client class savefile method."""

    def setUp(self):
        """Set up the Client object and a sample list of dictionaries for testing."""
        self.client = Client()
        self.listofdicts = [{"this": "one", "will": "be", "extra": "lonng", "forr": "testting", "sake": "ahaha", "longwordscuzwhynot": "letsseeifcanhandle"}]

    def test_savefile_json(self):
        """
        Test savefile method for JSON file format.

        This test case mocks the user input, calls the savefile method of the Client class
        with a sample list of dictionaries and file format as 'JSON'. It then checks if the
        contents of the saved file match the expected JSON representation of the list of dictionaries.
        """
        with patch('builtins.input', side_effect=["test_json"]):
            filename = self.client.savefile(self.listofdicts, "JSON")
            with open(filename, "r") as jsonfile:
                contents = jsonfile.read()
            expected_contents = '[{"this": "one", "will": "be", "extra": "lonng", "forr": "testting", "sake": "ahaha", "longwordscuzwhynot": "letsseeifcanhandle"}]'
            self.assertEqual(contents, expected_contents)

    def test_savefile_binary(self):
        """
        Test savefile method for Binary file format.

        This test case mocks the user input, calls the savefile method of the Client class
        with a sample list of dictionaries and file format as 'Binary'. It then checks if the
        contents of the saved file match the expected binary representation of the list of dictionaries.
        """
        with patch('builtins.input', side_effect=["test_binary"]):
            filename = self.client.savefile(self.listofdicts, "Binary")
            with open(filename, "rb") as binfile:
                contents = binfile.read()
            expected_contents = b'\x80\x04\x95|\x00\x00\x00\x00\x00\x00\x00]\x94}\x94(\x8c\x04this\x94\x8c\x03one\x94\x8c\x04will\x94\x8c\x02be\x94\x8c\x05extra\x94\x8c\x05lonng\x94\x8c\x04forr\x94\x8c\x08testting\x94\x8c\x04sake\x94\x8c\x05ahaha\x94\x8c\x12longwordscuzwhynot\x94\x8c\x12letsseeifcanhandle\x94ua.'
            self.assertEqual(contents, expected_contents)

    def test_savefile_xml(self):
        """
        Test savefile method for XML file format.

        This test case mocks the user input, calls the savefile method of the Client class
        with a sample list of dictionaries and file format as 'XML'. It then checks if the
        contents of the saved file match the expected XML representation of the list of dictionaries.
        """
        with patch('builtins.input', side_effect=["test_xml"]):
            filename = self.client.savefile(self.listofdicts, "XML")
            with open(filename, "r") as xmlfile:
                contents = xmlfile.read()
            expected_contents = '<?xml version="1.0" encoding="UTF-8" ?><root><item><this>one</this><will>be</will><extra>lonng</extra><forr>testting</forr><sake>ahaha</sake><longwordscuzwhynot>letsseeifcanhandle</longwordscuzwhynot></item></root>'
            self.assertEqual(contents, expected_contents)

if __name__ == "__main__":
    unittest.main()
