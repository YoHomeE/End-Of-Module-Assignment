import socket               # Import socket module
import threading            # Import threading module for connecting multiple clients 
import pickle               # Import picke module for serialization
import json                 # Import json module to handle JSON objects
import ast                  # Import ast module for formatting
import os                   # Import os module for saving files in a specific directory

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


    def start_server(self):
        self.host_socket.bind(self.ADDR)
        self.host_socket.listen()
        print('Server is listening...')
        # A loop to accept multiple connections
        while True:
            try:
                conn, addr = self.host_socket.accept()
                print(f"New connection from {addr} is established.")
                #create separate threads for new connections
                threading.Thread(target=self.handle_client,
                                 args=(conn, addr)).start()
            except ConnectionError:
                print('Connection Error!')


    def handle_client(self, conn, addr):
        data = conn.recv(SIZE)                  #Receive data from Client
        received = data.decode("utf-8")         #Decode data
        result = ast.literal_eval(received)     #Access data as a dictionary
    
        filename = result['file']               #Access filename from incoming data
        content_type = result['type']           #Access file type from incoming data
 
        '''Saving the file in directory'''
        directory_name = 'received_files'       
        if not os.path.exists(directory_name):  #Create directory if absent
            os.makedirs(directory_name)
        
        if content_type == 'JSON':              #Extracting data from JSON file
            with open(directory_name + '/' + filename, "w") as f:
                f.write(result['data'])
                f.close()
                print('The file has been saved in the [received_files] folder')

        elif content_type == 'Binary':          #Extracting data from Binary file
            with open(directory_name + '/' + filename, "wb") as f:
                f.write(result['data'])
                f.close()
                print('The file has been saved in the [received_files] folder')

        """ Closing the connection"""
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")




if __name__ == "__main__":
    server = Server()
    server.start_server()
