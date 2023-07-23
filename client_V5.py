import socket
import json
import pickle
import dicttoxml
import string
import os
import encryption

BUFFER_SIZE = 4096
FORMAT = "utf-8"
encrypt_status = False


class Client:
    def __init__(self):
        """
        Initialize the Client class.
        """
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.dict = [{}]
        self.client_socket = None
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        """
        Connect to the server using the specified address and port.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        print(f"Connecting to server on {self.server} on Port {self.port}")

        try:
            self.client.connect(self.ADDR)
            self.client_socket = self.client.makefile("wb")
            print("You have successfully connected.")
            return True
        except ConnectionRefusedError:
            print(
                f"Connection failed. Please make sure there is a server running on IP {self.server}: Port {self.port}"
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
        group_members = []

        for member in range(num_members):
            details = {}
            for k in range(num_keys):
                key = input("Please Enter your Key: ")
                value = input("Please enter your value: ")
                details[key] = value
            group_members.append(details)
        return group_members

    def savefile(self, group_members, selection):
        """
        Save the group_members dictionary to a file based on the selection format.

        Args:
            group_members (list): The list of dictionaries to save.
            selection (str): The format to save the data as (JSON, Binary, or XML).

        Returns:
            str: The name of the saved file.
        """
        if selection == "JSON":
            filename = input("Please name your file (Do not add the .format) : ")
            filename += ".json"
            with open(filename, "w") as jsonfile:
                jsonfile.write(json.dumps(group_members))
                print("Successfully saved dictionary in JSON with name", filename)
            with open(filename, "r") as jsonfile:
                contents = jsonfile.read()
                print(contents)
                return filename

        elif selection == "Binary":
            filename = input("Please name your file (The code with add the .format) : ")
            filename += ".pkl"
            with open(filename, "wb") as binfile:
                pickle.dump(group_members, binfile)
                print("Dictionary successfully saved in Binary with name", filename)
            with open(filename, "rb") as binfile:
                contents = binfile.read()
                print(contents)
                return filename

        elif selection == "XML":
            filename = input("Please name your file (The code with add the .format) : ")
            filename += ".xml"
            xml_string = dicttoxml.dicttoxml(group_members, attr_type=False)
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
    if client.connect_to_server():
        num_members = int(input("Please enter the number of Dictionaries: "))
        num_keys = int(input("Please enter the number of Keys: "))
        group_members = client.createdict(num_members, num_keys)
        print("Is this the dictionary you wanted?")
        print(group_members)

        encrypt_values = input("Encrypt values? (Yes/No): ").lower()
        while encrypt_values not in ["yes", "no"]:
            print("Invalid input. Please enter either 'Yes' or 'No'.")
            encrypt_values = input("Encrypt values? (Yes/No): ").lower()

        if encrypt_values == "yes":
            group_members = encryption.encrypt_list_of_dicts(group_members)
            encrypt_status = True

        else:
            print("Skipping encryption. Proceeding with the original dictionary.")

        while True:
            selection = input("Please select pickle format: JSON, Binary, or XML: ")
            if selection in ["JSON", "Binary", "XML"]:
                filename = client.savefile(group_members, selection)
                break
            else:
                print(
                    "Invalid selection. Please choose either 'JSON', 'Binary', or 'XML'."
                )

        send_to_server = input("Would you like to send the file to the server?")
        if send_to_server == "Yes":
            client.send_file(filename, encrypt_status)
        else:
            print("Send file canceled.")
