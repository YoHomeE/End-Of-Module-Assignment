import unittest
import socket
import threading
from unittest.mock import Mock, patch
from server import Server

class TestServer(unittest.TestCase):
    """Test cases for the Server class."""

    def test_handle_client(self):
        # Create a mock socket object and mock the bind and listen methods
        mock_socket = Mock(spec=socket.socket)
        mock_socket.bind.return_value = None
        mock_socket.listen.return_value = None

        # Create a mock connection and address
        mock_conn = Mock(spec=socket.socket)
        mock_addr = ("127.0.0.1", 12345)

        # Patch the necessary functions for the server to avoid real network calls
        with patch("socket.socket", return_value=mock_socket):
            with patch("socket.gethostbyname", return_value="127.0.0.1"):
                # Initialize the server
                server = Server()

                # Mock threading.active_count() to return 1 (main thread)
                with patch("threading.active_count", return_value=1):
                    # Simulate a new connection
                    with patch.object(server, "handle_client", return_value=None) as mock_handle_client:
                        # Start the server in a separate thread
                        server_thread = threading.Thread(target=server.start_server)
                        server_thread.start()

                        # Assert that the server socket is bound and listening
                        mock_socket.bind.assert_called_once_with(("127.0.0.1", 5050))
                        mock_socket.listen.assert_called_once()

                        # Simulate a new connection
                        mock_socket.accept.return_value = (mock_conn, mock_addr)
                        mock_socket.accept.side_effect = [(mock_conn, mock_addr), ConnectionError]

                        # Wait for a short time to allow the server thread to accept the connection
                        server_thread.join(timeout=0.1)

                        # Assert that the server handled the client
                        mock_handle_client.assert_called_once_with(mock_conn, mock_addr)

                        # Stop the server thread
                        server_thread.join()

if __name__ == "__main__":
    unittest.main()
