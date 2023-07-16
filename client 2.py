import socket
import json
import pickle

HEADER = 1064
# HEADER message, buffer the bytesize of first msg recevied
FORMAT = "utf-8"
# for decoding the messages


class Client:
    def __init__(self):
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.dict = [{}]
        self.client_socket = None
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        print(f"Connecting to server on {self.server} on Port {self.port} ")

        try:
            self.client.connect(self.ADDR)
            print("You have succesfully connected.")
            return True
        except ConnectionRefusedError:
            print(
                f"Connection failed, please make sure there is a server \
                  running on IP {self.server}: Port {self.port} "
            )
            return False

    def disconnect(self):
        if self.client is not None:
            disconnect = input("Would you like to disconnect : ")
            if disconnect == "Yes":
                self.client.close()

    def createdict(self, num_members):
        group_members = []

        for member in range(num_members):
            details = {
                "Name": input(f"Please enter Student Name(member{member+1}): "),
                "Surname": input(f"Please enter Student Surname(member{member+1}): "),
                "Project Role": input(f"Please enter Project Role(member{member+1}): "),
            }
            group_members.append(details)
        file_name = input("Please enter the file name: ")
        return [group_members, file_name]

    def send_string(self, msg):
        """
        send message to the server
        :param msg: message to be sent
        :return: None
        """
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        # make up to 64byte message length
        # standardize the first message sent to server
        self.client.send(send_length)
        self.client.send(message)

    def rec_string(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        # receive the length of the message
        if msg_length:
            msg_length = int(msg_length)
            # convert the msg_length to integer
            msg = self.client.recv(msg_length).decode(FORMAT)
            # receive the actual message for the exact byte length
            print(f"msg from server: {msg}")

    def send_file(self, filename, selection):
        """
        load the selected file as b msg, and send to server
        return: None
        """
        self.send_string(filename)
        self.send_string(selection)
        if selection == "JSON":
            with open(f"{filename}.json", "r") as file:
                msg = json.load(file)
            msg = json.dumps(msg).encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            # make up to  message length
            # standardize the first message sent to server
            self.client.send(send_length)
            self.client.send(msg)
        elif selection == "Binary":
            # send the pickled file to server
            with open(f"{filename}.pkl", "rb") as file:
                msg = pickle.load(file)
            msg = pickle.dumps(msg)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            # make up to  message length
            # standardize the first message sent to server
            self.client.send(send_length)
            self.client.send(msg)

    def savefile(self, group_members, file_name, selection):
        if selection == "JSON":
            # save file locally as JSON
            with open(f"{file_name}.json", "w") as jsonfile:
                json.dump(group_members, jsonfile)
                print("Successfully saved dictionary as JSON")
            # print file to screen
            with open(f"{file_name}.json", "r") as jsonfile:
                contents = jsonfile.read()
                print(contents)

        elif selection == "Binary":
            with open(f"{file_name}.pkl", "wb") as binfile:
                pickle.dump(group_members, binfile)
                print("Dictionary successfully saved as Binary File")
            with open(f"{file_name}.pkl", "rb") as binfile:
                contents = binfile.read()
                print(contents)

        else:
            print("Invalid selection. Please choose either 'JSON' or 'Binary'.")


if __name__ == "__main__":
    client = Client()
    if client.connect_to_server():
        num_members = int(input("Please enter the number of group members: "))
        values = client.createdict(num_members)
        group_members = values[0]
        filename = values[1]
        print(group_members)
        print(f"filename: {filename}")

        while True:
            selection = input("Please select pickle format: JSON, Binary or XML: ")
            if selection in ["JSON", "Binary"]:
                client.savefile(group_members, filename, selection)
                break
            else:
                print("Invalid selection. Please choose either 'JSON' or 'Binary'.")
        while True:
            decision = input("Would you like to send file and save to server? ")
            if decision in ["Yes", "No"]:
                if decision == "Yes":
                    client.send_file(filename=filename, selection=selection)
                elif decision == "No":
                    print("File not sent.")
                break
            else:
                print("Invalid selection. Please choose either 'Yes' or 'No'.")
        """selection = input("Please select pickle format: JSON, Binary or XML : ")
        client.savefile(group_members, selection)"""


"""def send(msg):
    
    send message to the server
    :param msg: message to be sent
    :return: None
 
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    # make up to 64byte message length
    # standardize the first message sent to server
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


send("Hello World!")"""
