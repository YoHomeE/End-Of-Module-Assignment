import socket  # Import socket module
import threading  # Import threading module for connecting multiple clients
import pickle  # Import picke module for serialization
import json  # Import json module to handle JSON objects
import dicttoxml # Importing xml objects
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
        def send_data(msg: str):
            """
            encode str -> byte data, send to the client
            """
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (SIZE - len(send_length))
            # make up to header message length
            conn.send(send_length)
            conn.send(message)

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

        def receive_metadata():
            # receive filename
            filename = receive_data()
            filetype = filename.split(".")[-1]
            file_content = conn.recv(SIZE)

            metadata = {
                "file_name": filename,
                "file_type": filetype,
                "content": file_content,
            }
            print(f"data from client {addr} received \n {metadata}")
            send_data("metadata received")
            return metadata

        def save_to_file(metadata):
            file_name = metadata["file_name"]
            file_type = metadata["file_type"]
            content = metadata["content"]
            if file_type == "json":
                with open(self.directory_name + "/" + file_name, "w") as jsonfile:
                    loaded = json.loads(content)
                    json.dump(loaded, jsonfile)
                    print(
                        "Successfully saved dictionary in JSON with name",
                        file_name,
                    )
                with open(self.directory_name + "/" + file_name, "r") as jsonfile:
                    contents = jsonfile.read()
                    print(contents)

            elif file_type == "pkl":
                with open(self.directory_name + "/" + file_name, "wb") as binfile:
                    binfile.write(content)
                    print(
                        "Dictionary successfully saved in Binary with name", file_name
                    )
                with open(self.directory_name + "/" + file_name, "rb") as binfile:
                    contents = binfile.read()
                with open(file_name, "rb") as binfile:
                    original = binfile.read()
                print("server copy == original copy?", contents == original)

            elif file_type == "xml":
                with open(self.directory_name + "/" + file_name, "w") as xmlfile:
                    xmlfile.write(content.decode(FORMAT))
                    print("Successfully saved dictionary in XML with name", file_name)
                with open(self.directory_name + "/" + file_name, "r") as xmlfile:
                    contents = xmlfile.read()
                    print(contents)

            msg = f"The file has been saved on SERVER at [{self.directory_name}] folder"
            send_data(msg)

        # start
        # calling the functions
        #       received = receive_data()  # Access data from client
        #       save_data(self, received)  # Save data to server

        """ Closing the connection"""
        metadata_received = receive_metadata()
        save_to_file(metadata_received)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


if __name__ == "__main__":
    server = Server()
    server.start_server()
