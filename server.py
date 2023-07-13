import socket
import threading
import time

# threading -> create a new thread everytime a new connection

HEADER = 64
# HEADER message, buffer the bytesize of first msg recevied
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

    def send_msg(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        # make up to 64byte message length
        # standardize the first message sent to server
        conn.send(send_length)
        conn.send(message)

    def rec_msg():
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

            send_msg(msg="Msg received")
            # conn.send("Msg received".encode(FORMAT))

    connected = True
    while connected:
        rec_msg()

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
