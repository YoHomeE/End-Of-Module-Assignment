import socket
import threading
import json
import pickle

# server.py

# threading -> create a new thread everytime a new connection

HEADER = 1064
# HEADER message, standardize the bytesize of first msg recevied
PORT = 5050
# specify a port no.
SERVER = socket.gethostbyname(socket.gethostname())
# get the localhost ip address for hosting server
ADDR = (SERVER, PORT)
# assign the address
FORMAT = "utf-8"
# for decoding the messages
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
# create a server and bind the server to address above


def handle_client(conn, addr):
    """
    handle the connection with each clients
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    def rec_string_msg():
        """
        receive string message from client
        return: None

        """
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # receive the length of the message
        if msg_length:
            msg_length = int(msg_length)
            # convert the msg_length to integer
            msg = conn.recv(msg_length).decode(FORMAT)
            # receive the actual message for the exact byte length
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            return msg

    def rec_json_msg(file_name):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # receive the length of the message
        if msg_length:
            msg_length = int(msg_length)
            # convert the msg_length to integer
            msg = conn.recv(msg_length).decode(FORMAT)
            msg_loaded = json.loads(msg)
            # receive the actual message for the exact byte length
            print(f"json msg from client: {msg_loaded}")
            print(f"now saving to server")
            with open(f"server_file/{file_name}.txt", "w") as jsonfile:
                json.dump(msg_loaded, jsonfile)
                print("Successfully saved dictionary as JSON")

    def rec_pickled_msg(file_name):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # receive the length of the message
        if msg_length:
            msg_length = int(msg_length)
            # convert the msg_length to integer
            msg = conn.recv(msg_length)
            msg_loaded = pickle.loads(msg)
            # receive the actual message for the exact byte length
            print(f"pickled msg from client: {msg_loaded}")
            print(f"now saving to server")
            with open(f"server_file/{file_name}.pkl", "wb") as picklefile:
                pickle.dump(msg_loaded, picklefile)
                print("Successfully saved dictionary as JSON")

    def receive_file():
        # 1 to receive the file name
        # 2 to receive the file type
        # 3 to receive the file size
        # 4 to receive the file
        file_name = rec_string_msg()
        file_type = rec_string_msg()
        if file_type == "JSON":
            rec_json_msg(file_name)
        if file_type == "PICKLED":
            rec_pickled_msg(file_name)

    connected = True
    while connected:
        receive_file()
    #        msg_length = conn.recv(HEADER).decode(FORMAT)
    #        if msg_length:
    #            msg_length = int(msg_length)
    #            msg = conn.recv(msg_length).decode(FORMAT)
    #            if msg == DISCONNECT_MESSAGE:
    #                connected = False

    #            print(f"[{addr}] {msg}")

    #            conn.send("Msg received".encode(FORMAT))

    conn.close()


# start of server
def start():
    """
    start of server
    listening on a port with an infinite loop
    create a new thread every time a new client connects
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
