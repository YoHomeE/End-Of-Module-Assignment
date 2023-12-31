"""
Server Module
-------------

This module implements a simple file server that handles incoming client connections,
receives data, and saves files sent by the clients. It supports different file formats
(JSON, pickle, and XML) and can handle encrypted data.

The server class in this module utilizes socket programming and multithreading to listen
for incoming connections and handle multiple clients simultaneously.

Requirements:
    - Python 3.6+
    - socket
    - threading
    - pickle
    - json
    - dicttoxml
    - xml.etree.ElementTree
    - os
    - time
    - encryption (custom module for data encryption)


Classes:
    Server: The main server class that handles incoming connections and file handling.

Functions:
    No direct functions are exposed to the user. The server handles all client interactions.

Example:
    $ python server.py

Note:
    The "encryption" module must be present in the same directory or included in the Python
    path for handling encrypted data.

"""

import socket  # Import socket module
import threading  # Import threading module for connecting multiple clients
import pickle  # Import picke module for serialization
import json  # Import json module to handle JSON objects
import time
import os  # Import os module for saving files in a specific directory
import ast  # Import ast module for formatting
import xml.etree.ElementTree as ET
import dicttoxml
import encryption


SIZE = 4096
FORMAT = "utf-8"


class Server:
    """initialises the server with the necessary information to perform function"""

    def __init__(self):
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.addr = (self.server, self.port)
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.directory_name = "received_files"

        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

    def start_server(self):
        """Start the server and listen for incoming connections."""
        self.host_socket.bind(self.addr)
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

    def send_data(self, conn, msg: str):
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

    def receive_data(self, conn, addr):
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

    def receive_metadata(self, conn, addr):
        """Receive metadata sent by the client and return the metadata as a dictionary."""
        filename = self.receive_data(conn, addr)
        filetype = filename.split(".")[-1]
        encryption_status = self.receive_data(conn, addr)
        file_content = conn.recv(SIZE)
        receive_msg = "metadata received"

        if encryption_status == "encrypted":
            encryption_status = True
        else:
            encryption_status = False

        metadata = {
            "file_name": filename,
            "file_type": filetype,
            "content": file_content,
            "encryption_status": encryption_status,
        }
        print(f"data from client {addr} received \n {metadata}")

        self.send_data(conn, receive_msg)
        return metadata

    def save_to_file(self, metadata, conn, addr):
        """Save the received file to disk based on its type and encryption status."""
        file_name = metadata["file_name"]
        file_type = metadata["file_type"]
        content = metadata["content"]
        encryption_status = metadata["encryption_status"]
        if file_type == "json":
            with open(self.directory_name + "/" + file_name, "w") as jsonfile:
                loaded = json.loads(content)
                json.dump(loaded, jsonfile)
                print(
                    "Successfully saved dictionary in JSON with name",
                    file_name,
                )
            if encryption_status:
                decrypted_content = encryption.decrypt_list_of_dicts(loaded)
                with open(
                    self.directory_name + "/" + "decrypted_" + file_name, "w"
                ) as jsonfile:
                    json.dump(decrypted_content, jsonfile)
                print(
                    "Successfully saved decrypted dictionary in JSON with name decrypted_"
                    + file_name,
                )

        elif file_type == "pkl":
            with open(self.directory_name + "/" + file_name, "wb") as binfile:
                binfile.write(content)
                print("Dictionary successfully saved in Binary with name", file_name)
            if encryption_status:
                decrypted_content = encryption.decrypt_list_of_dicts(
                    pickle.loads(content)
                )
                with open(
                    self.directory_name + "/" + "decrypted_" + file_name, "wb"
                ) as binfile:
                    pickle.dump(decrypted_content, binfile)
                print(
                    "Successfully saved decrypted dictionary in Binary with name decrypted_"
                    + file_name,
                )

        elif file_type == "xml":
            with open(self.directory_name + "/" + file_name, "w") as xmlfile:
                xmlfile.write(content.decode(FORMAT))
                print("Successfully saved dictionary in XML with name", file_name)
            if encryption_status:
                root = ET.fromstring(content)
                list_of_dicts = []
                for elem in root.findall("item"):
                    dict_data = {}
                    for child in elem:
                        dict_data[child.tag] = child.text
                    list_of_dicts.append(dict_data)
                decrypted_content = encryption.decrypt_list_of_dicts(list_of_dicts)
                xml_string = dicttoxml.dicttoxml(decrypted_content, attr_type=False)
                with open(
                    self.directory_name + "/" + "decrypted_" + file_name, "w"
                ) as xmlfile:
                    xmlfile.write(xml_string.decode())
                    print(
                        "Successfully saved decrypted dictionary in XML with name decrypted_",
                        file_name,
                    )
                msg = f"The file has been saved on SERVER at [{self.directory_name}] folder"
                self.send_data(conn, msg)

    def handle_client(self, conn, addr):
        """Handle a client connection."""
        metadata_received = self.receive_metadata(conn, addr)
        self.save_to_file(metadata_received, conn, addr)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


if __name__ == "__main__":
    server = Server()
    server.start_server()
