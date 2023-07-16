import socket  # Import socket module
import threading  # Import threading module for connecting multiple clients
import pickle  # Import picke module for serialization
import json  # Import json module to handle JSON objects
import ast  # Import ast module for formatting
import os  # Import os module for saving files in a specific directory
import time

SIZE = 4096
FORMAT = "utf-8"


class Server:
    """initialises the server with the necessary information to perform function"""

    def __init__(self):
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.server, self.port)
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.directory_name = "received_files"

    def start_server(self):
        self.host_socket.bind(self.ADDR)
        self.host_socket.listen()
        print(f"[LISTENING] Server is listening on {self.server}")
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        # A loop to accept multiple connections
        while True:
            try:
                conn, addr = self.host_socket.accept()
                print(f"New connection from {addr} is established.")
                # create separate threads for new connections
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            except ConnectionError:
                print("Connection Error!")

    def handle_client(self, conn, addr):
        def receive_data():
            """
            receive byte data sent from client
            return: decoded msg
            """
            msg_length = conn.recv(SIZE).decode(FORMAT)
            # receive the data length in bytes
            if msg_length:  # avoid error with empty msg upon connection
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                # receive the actual message for the exact byte length
                print(f"[{addr}] {msg}")  # print to console for debugging
                return msg

        def save_data(self, received_data):
            """
            save the data received from client
            """
            result = ast.literal_eval(received_data)  # Access data as a dictionary

            filename = result["file"]  # Access filename from incoming data
            content_type = result["type"]  # Access file type from incoming data

            """Saving the file in directory"""

            if not os.path.exists(self.directory_name):  # Create directory if absent
                os.makedirs(self.directory_name)

            if content_type == "JSON":  # Extracting data from JSON file
                with open(self.directory_name + "/" + filename, "w") as f:
                    data_json = json.loads(result["data"])
                    print(f"json data received: {data_json}")
                    json.dump(data_json, f)
                    print(
                        f"The file has been saved in the [{self.directory_name}] folder"
                    )

            elif content_type == "Binary":  # Extracting data from Binary file
                with open(self.directory_name + "/" + filename, "wb") as f:
                    data_pickle = pickle.loads(result["data"])
                    print(f"binary data received: {data_pickle}")
                    pickle.dump(data_pickle, f)
                    print(
                        f"The file has been saved in the [{self.directory_name}] folder"
                    )

        received = receive_data()  # Access data from client
        save_data(self, received)  # Save data to server

        """ Closing the connection"""
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


if __name__ == "__main__":
    server = Server()
    server.start_server()
