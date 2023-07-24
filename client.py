"""
Client Module
-------------

This module implements a client application that 
allows users to create dictionaries with user-input keys and values.
The client can choose to encrypt the dictionary 
values using a simple substitution cipher.
The client can save the created dictionary in JSON, Binary, or XML format.
Additionally, the client can send the saved file to a connected server.

Requirements:
    - Python 3.6+
    - socket
    - json
    - pickle
    - string
    - os
    - dicttoxml
    - encryption (custom module for data encryption)

Functions:
    intexception(prompt: str) -> int:
        Function to handle integer input with exception handling.

Classes:
    Client:
        The main client class that handles dictionary creation, 
        saving files, and sending files to the server.

Usage:
    - Run the python3 client.py when the server is running
    - The client will display a welcome message and 
      provide instructions on how to use the program.
    - Follow the prompts to create dictionaries, 
      save them in the desired format, and optionally encrypt the values.
    - If encryption is chosen, the client will use 
      the "encryption" module to encrypt the dictionary values.
    - The client can send the saved file to the connected server for further processing.

Example:
    $ python3 client.py

Note:
    The "encryption" module must be present in the 
    same directory or included in the Python path for handling encrypted data.

"""
import socket
import json
import pickle
import string
import os
import dicttoxml

import encryption

BUFFER_SIZE = 4096
FORMAT = "utf-8"
ENCRYPT_STATUS = False

def intexception(prompt):
    """
    Function to handle integer input with exception handling.

    Args:
        prompt (str): The prompt message for user input.

    Returns:
        int: The valid integer entered by the user.
    """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Invalid input, please enter a non-negative number")
            else:
                return value
        except ValueError:
            print("Invalid input, please enter an integer.")


class Client:
    """
    Represents a client-side application to create dictionaries, optionally encrypt their
    keys and values, save them in JSON, Binary, or XML format, and send the file to a server.

    Attributes:
        header (int): The header size for messages sent to the server.
        port (int): The port number for the server communication.
        server (str): The server address (IP address or hostname).
        dict (list): A list containing dictionaries created by the user.
        client_socket (file object): The socket file object for communication with the server.
        addr (tuple): A tuple containing the server address and port.
        client (socket object): The client-side socket object.
    """
    def __init__(self):
        """
        Initialize the Client class.
        """
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.dict = [{}]
        self.client_socket = None
        self.addr = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def help_function(self):
        """
        Display information about how to use the program.
        """
        print("Welcome to the Client program.")
        print("This program allows you to create dictionaries with user-input keys and values.")
        print("You can choose to encrypt the dictionary keys \
            and values using a simple substitution cipher.")
        print("After creating the dictionary, you can save it in JSON, Binary, or XML format.")
        print("Finally, you can choose to send the saved file to the connected server.")
        print("To use the program, follow these steps:")
        print("1. Enter the number of dictionaries you want to create.")
        print("2. Enter the number of keys to include in each dictionary.")
        print("3. Provide the keys and values for each dictionary.")
        print("4. Optionally, choose to encrypt the values.")
        print("5. Select the format (JSON, Binary, or XML) to save the data.")
        print("6. If you choose to send the file to the server, it will be transferred.")
        print("7. To exit the program, use 'ctrl + c' at any time.")
        print("Enjoy using the Client program!")
        print("To proceed with the program, simply follow the prompts below.")

    def run(self):
        """
        Start the client application and display the help message if requested.
        """
        while True:
            display_help = input("Would you like help on how to use the program? (Yes/No): ")
            if display_help == "Yes":
                self.help_function()
                return
            elif display_help == "No":
                break
            else:
                print("Invalid Selection, Please choose either Yes or No")


    def connect_to_server(self):
        """
        Connect to the server using the specified address and port.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        print(f"Connecting to server on {self.server} on Port {self.port}")

        try:
            self.client.connect(self.addr)
            self.client_socket = self.client.makefile("wb")
            print("You have successfully connected.")
            return True
        except ConnectionRefusedError:
            print(
                f"Connection failed. Please make sure there \
                    is a server running on IP {self.server}: Port {self.port}"
            )
            return False

    def send_data(self, msg: str):
        """
        encode str to byte
        send byte data to the server
        send a header msg of byte length
        """
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (BUFFER_SIZE - len(send_length))
        # make up to header message length
        self.client.sendall(send_length)
        self.client.sendall(message)

    def receive_data(self):
        """
        receive byte data sent from server
        return: decoded msg
        """
        msg_length = self.client.recv(BUFFER_SIZE).decode(FORMAT)
        # receive the data length in bytes
        if msg_length:  # avoid error with empty msg upon connection
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(FORMAT)
            # receive the actual message for the exact byte length
            print(f"[SERVER] {msg}")  # print to console for debugging
            return msg

    def createdict(self, num_members, num_keys):
        """
        Create a dictionary with user-input keys and values.

        Args:
            num_members (int): The number of dictionaries to create.
            num_keys (int): The number of keys to include in each dictionary.

        Returns:
            list: A list containing the created dictionaries.
        """
        listofdicts = [] #Named Variable list of Dicts from Group Members

        for member in range(num_members):
            details = {}
            for k in range(num_keys):
                key = input("Please Enter your Key: ")
                value = input("Please enter your value: ")
                details[key] = value
            listofdicts.append(details)
        return listofdicts

    def savefile(self, listofdicts, selection):
        """
        Save the listofdicts dictionary to a file based on the selection format.

        Args:
            listofdicts (list): The list of dictionaries to save.
            selection (str): The format to save the data as (JSON, Binary, or XML).

        Returns:
            str: The name of the saved file.
        """
        if selection == "JSON":
            filename = input("Please name your file (Do not add the .format) : ")
            filename += ".json"
            with open(filename, "w") as jsonfile:
                jsonfile.write(json.dumps(listofdicts))
                print("Successfully saved dictionary in JSON with name", filename)
            with open(filename, "r") as jsonfile:
                contents = jsonfile.read()
                print(contents)
                return filename

        elif selection == "Binary":
            filename = input("Please name your file (The code with add the .format) : ")
            filename += ".pkl"
            with open(filename, "wb") as binfile:
                pickle.dump(listofdicts, binfile)
                print("Dictionary successfully saved in Binary with name", filename)
            with open(filename, "rb") as binfile:
                contents = binfile.read()
                print(contents)
                return filename

        elif selection == "XML":
            filename = input("Please name your file (The code with add the .format) : ")
            filename += ".xml"
            xml_string = dicttoxml.dicttoxml(listofdicts, attr_type=False)
            with open(filename, "w") as xmlfile:
                xmlfile.write(xml_string.decode())
                print("Successfully saved dictionary in XML with name", filename)
            with open(filename, "r") as xmlfile:
                contents = xmlfile.read()
                print(contents)
                return filename

        else:
            print("Invalid selection. Please choose either 'JSON', 'Binary', or 'XML'.")

    def send_file(self, filename, encryption_status):
        """
        Send a file to the connected server.

        Args:
            filename (str): The name of the file to be sent.

        Raises:
            FileNotFoundError: If the specified file does not exist.

        Returns:
            None
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        # Encode the metadata and send it as bytes by calling send_data function
        metadata_filename = filename
        self.send_data(metadata_filename)  # send filename
        if encryption_status == True:
            metadata_encrypt_status = "encrypted"
        else:
            metadata_encrypt_status = "not encrypted"
        self.send_data(metadata_encrypt_status)
        with open(filename, "rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)  # read with BUFFER SIZE
                if not bytes_read:
                    # Transfer is done. Nothing left to be sent.
                    break
                # Send what has been read so far.
                self.client.sendall(bytes_read)

        print(f"{filename} was sent to the server.")
        self.receive_data()  # receive confirmation from server for metadata
        self.receive_data()  # receive confirmation from server for file saving


if __name__ == "__main__":
    client = Client()
    client.run()
    if client.connect_to_server():
        num_members = intexception("Please enter the number of Dictionaries: ")
        # Updated to use intexception function to prevent and loop back upon invalid entry
        num_keys = intexception("Please enter the number of Keys: ")
        listofdicts = client.createdict(num_members, num_keys)
        print("Is this the dictionary you wanted?")
        print(listofdicts)

        encrypt_values = input("Encrypt values? (Yes/No): ")
        while encrypt_values not in ["Yes", "No"]:
            print("Invalid input. Please enter either 'Yes' or 'No'.")
            encrypt_values = input("Encrypt values? (Yes/No): ")

        if encrypt_values == "Yes":
            listofdicts = encryption.encrypt_list_of_dicts(listofdicts)
            ENCRYPT_STATUS = True

        else:
            print("Skipping encryption. Proceeding with the original dictionary.")

        while True:
            selection = input("Please select pickle format: JSON, Binary, or XML: ")
            if selection in ["JSON", "Binary", "XML"]:
                filename = client.savefile(listofdicts, selection)
                break
            else:
                print(
                    "Invalid selection. Please choose either 'JSON', 'Binary', or 'XML'."
                )

        send_to_server = input("Would you like to send the file to the server ? (Yes/No) : ")
        if send_to_server == "Yes":
            client.send_file(filename, ENCRYPT_STATUS)
        else:
            print("Send file canceled.")
