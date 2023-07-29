import unittest
from unittest.mock import patch, MagicMock, call
from server_testing import Server


class TestServer(unittest.TestCase):
    """Test cases for the Server class."""

    def setUp(self):
        self.server = Server()

    def test_send_data(self):
        # Create a mock connection
        mock_conn = MagicMock()

        # Call the send_data method
        self.server.send_data(mock_conn, "Test Message")

        # Assert that the send method of the mock connection was called twice (send msg length, send msg itself)
        self.assertEqual(mock_conn.send.call_count, 2)

    def test_receive_data(self):
        # Create a mock connection
        mock_conn = MagicMock()

        # Set up the mock connection to return the byte length as a string when recv is called
        mock_conn.recv.side_effect = [b"10", b"Test Data"]

        # Call the receive_data method
        data = self.server.receive_data(mock_conn, "Test Address")

        # Define the expected calls to recv with the correct buffer size
        expected_calls = [
            call(4096),  # First call with buffer size
            call(10),  # Second call with the byte length received from the first call
        ]

        # Assert that the recv method of the mock connection was called twice with the correct buffer size
        mock_conn.recv.assert_has_calls(expected_calls)

        # Assert that the received data is as expected
        self.assertEqual(data, "Test Data")

    def test_receive_metadata(self):
        # Create a mock connection
        mock_conn = MagicMock()

        # Set up the mock connection to return the test data
        mock_conn.recv.side_effect = [
            b"14",  # Length of filename
            b"testfile.json",  # Filename
            b"9",  # Length of encryption status
            b"encrypted",  # Encryption status
            b"Test file content",  # File content
        ]

        # Call the receive_metadata method
        metadata = self.server.receive_metadata(mock_conn, "Test Address")

        # Assert that the recv method of the mock connection was called with the correct buffer size
        mock_conn.recv.assert_called_with(4096)

        # Assert the received metadata dictionary
        expected_metadata = {
            "file_name": "testfile.json",
            "file_type": "json",
            "content": b"Test file content",
            "encryption_status": True,
        }
        self.assertEqual(metadata, expected_metadata)

        # Assert that the send_data method was called to send the response message
        self.assertEqual(mock_conn.send.call_args[0][0], "metadata received".encode())

    def test_save_json_file(self):
        # Create mock metadata for a JSON file
        metadata = {
            "file_name": "testfile.json",
            "file_type": "json",
            "content": b'{"key": "value"}',
            "encryption_status": False,
        }

        # Create a mock connection
        mock_conn = MagicMock()

        # Call the save_to_file method
        with patch("builtins.open", create=True) as mock_open:
            self.server.save_to_file(metadata, mock_conn, "Test Address")

        # Assert that the correct file was opened with the correct mode
        mock_open.assert_called_once_with("received_files/testfile.json", "w")

    def test_save_pickle_file(self):
        # Create mock metadata for a pickle file
        metadata = {
            "file_name": "testfile.pkl",
            "file_type": "pkl",
            "content": b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03key\x94\x8c\x05value\x94u.",
            "encryption_status": False,
        }

        # Create a mock connection
        mock_conn = MagicMock()

        # Call the save_to_file method
        with patch("builtins.open", create=True) as mock_open:
            self.server.save_to_file(metadata, mock_conn, "Test Address")

        # Assert that the correct file was opened with the correct mode
        mock_open.assert_called_once_with("received_files/testfile.pkl", "wb")

    def test_save_xml_file(self):
        # Create mock metadata for an XML file
        metadata = {
            "file_name": "testfile.xml",
            "file_type": "xml",
            "content": b"<root><item><key>value</key></item></root>",
            "encryption_status": False,
        }

        # Create a mock connection
        mock_conn = MagicMock()

        # Call the save_to_file method
        with patch("builtins.open", create=True) as mock_open:
            self.server.save_to_file(metadata, mock_conn, "Test Address")

        # Assert that the correct file was opened with the correct mode
        mock_open.assert_called_once_with("received_files/testfile.xml", "w")


if __name__ == "__main__":
    unittest.main()
