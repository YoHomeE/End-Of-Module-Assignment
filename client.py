import socket
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# create the client
client.connect(ADDR)
# connect client to the server


def send(msg):
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
    client.send(send_length)
    client.send(message)


def rec_msg():
    msg_length = client.recv(HEADER).decode(FORMAT)
    # receive the length of the message
    if msg_length:
        msg_length = int(msg_length)
        # convert the msg_length to integer
        msg = client.recv(msg_length).decode(FORMAT)
        # receive the actual message for the exact byte length
        print(msg)


#    msg = client.recv(2048).decode(FORMAT)
#    print(msg)


send("Hello World!")
while True:
    time.sleep(3)
    send(f"time now is {time.time()}")
    rec_msg()
