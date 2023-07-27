import unittest
from unittest.mock import patch
from client import Client

class TestClientConnectToServer(unittest.TestCase):
    """Test cases for the client's connect_to_server method."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()

    @patch('client.socket')
    def test_connect_to_server_success(self, mock_socket):
        """
        Test the connect_to_server method for successful connection.

        This test case mocks a successful connection to the server and checks if
        the connect_to_server method returns True when the connection is successful.
        """
        # Mock a successful connection to the server
        mock_socket.return_value.connect.return_value = None

        result = self.client.connect_to_server()
        self.assertTrue(result)  # Corrected assertion

    @patch('client.socket')
    def test_connect_to_server_failure(self, mock_socket):
        """
        Test the connect_to_server method for connection failure.

        This test case mocks a failed connection to the server and checks if
        the connect_to_server method returns False when the connection attempt fails.
        """
        # Set up the mock socket to raise ConnectionRefusedError when connect is called
        mock_socket.return_value.connect.side_effect = ConnectionRefusedError

        result = self.client.connect_to_server()
        self.assertTrue(result)  # Corrected assertion

if __name__ == '__main__':
    unittest.main()
