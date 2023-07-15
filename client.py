import socket
import json
import pickle

"""Creates a class of Client, containing all the function thats clients should perform"""
class Client:
    """initialises the client with the necessary information to perform function"""
    def __init__(self):
        self.header = 64
        self.port = 5050
        self.server = socket.gethostbyname(socket.gethostname())
        self.dict = [{}] 
        self.client_socket = None
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """Connects the client to the server"""
    def connect_to_server(self):
        print(f'Connecting to server on {self.server} on Port {self.port} ') #f strings for dynamic updates

        try:
            self.client.connect(self.ADDR) #attempts connection
            print("You have succesfully connected.")
            return True
        except ConnectionRefusedError: #code for failing to connect
            print(f"Connection failed, please make sure there is a server \
                  running on IP {self.server}: Port {self.port} ")
            return False


    #def disconnect(self): I have commented out this code as it is not doing anything yet, have not completed it
        #if self.client is not None:
            #disconnect = input("Would you like to disconnect : ")
            #if disconnect == "Yes":
                #self.client.close()

    """Creates the dictionary - Going to work on making the keys dynamic(Inputs)"""
    def createdict(self, num_members):
        group_members = []

        for member in range(num_members):
            details = {
                'Name': input("Please enter Student Name: "),
                'Surname': input("Please enter Student Surname: "),
                'Project Role': input("Please enter Project Role: ")
            }
            group_members.append(details)
        return group_members

    def savefile(self, group_members, selection): #Saves the file into JSON and Binary so far
        if selection == "JSON":
            with open("group-members.txt", 'w') as jsonfile:
                jsonfile.write(json.dumps(group_members))
                print("Successfully saved dictionary as JSON")
            with open("group-members.txt", 'r') as jsonfile:
                contents = jsonfile.read()
                print(contents)

        elif selection == "Binary":
            with open("group-members.pkl", 'wb') as binfile:
                pickle.dump(group_members, binfile)
                print('Dictionary successfully saved as Binary File')
            with open("group-members.pkl", 'rb') as binfile:
                contents = binfile.read()
                print(contents)
        else: #Not sure if this is necessary now that it is in the __name__= __main__ but supposed to be text for invalid entry
            print("Invalid selection. Please choose either 'JSON' or 'Binary'.")

"""Engine behind the code, performs all the functions included in the class"""
if __name__ == "__main__":
    client = Client()
    if client.connect_to_server():
        num_members = int(input("Please enter the number of group members: "))
        group_members = client.createdict(num_members)
        print(group_members)

        while True:
            selection = input("Please select pickle format: JSON, Binary or XML: ")
            if selection in ["JSON", "Binary"]:
                client.savefile(group_members, selection)
                break
            else:
                print("Invalid selection. Please choose either 'JSON' or 'Binary'.")
