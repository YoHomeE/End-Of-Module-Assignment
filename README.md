# Substitution Cipher Server-Client Application

## Project Description

The Substitution Cipher Server-Client Application is a simple yet powerful tool that allows users to create dictionaries, optionally encrypt their keys and values using a substitution cipher, save the dictionaries in JSON, Binary, or XML format, and send the files to a connected server. The server then receives the files, saves them, and can optionally decrypt the encrypted files. This application is particularly useful when users need to securely transfer dictionaries between clients and a central server while maintaining the confidentiality of sensitive data.

## How to Install and Run the Project

To use the Substitution Cipher Server-Client Application, follow these steps:

1. Ensure that you have Python installed on your system.

2. Download or clone the project repository from GitHub.

3. Open a terminal or command prompt.

4. Navigate to the directory containing the server file (`server.py`).

5. Run the server by executing the following command in your terminal:

`python3 server.py`

The server will start running and display the listening address and active connections.

6. In another terminal or command prompt, navigate to the directory containing the client file (`client.py`).

7. Run the client by executing the following command:

`python3 client.py`

The client application will start running and display a welcome message and instructions on how to use the program.

8. Follow the prompts in the client application to create dictionaries, save them in JSON, Binary, or XML format, and optionally send the files to the connected server.

9. If you choose to send the file to the server, ensure that the server is running and reachable at the specified address and port.

## How to Use the Project

The Substitution Cipher Server-Client Application provides an easy-to-use interface for creating dictionaries and managing files. Follow the prompts in the client application to perform the following actions:

1. **Create Dictionaries:** Enter the number of dictionaries you want to create, followed by the number of keys to include in each dictionary. Provide the keys and values for each dictionary interactively.

2. **Encrypt Values (Optional):** You can choose to encrypt the values in the dictionaries using a substitution cipher. Enter "Yes" when prompted if you want to encrypt values; otherwise, enter "No" to skip encryption.

3. **Save Files:** Choose the format (JSON, Binary, or XML) to save the dictionaries. The application will prompt you to enter the desired filename. The saved files will be stored in the project directory.

4. **Send Files to Server (Optional):** If you want to send the saved files to the connected server, enter "Yes" when prompted. The application will transfer the files to the server. Otherwise, enter "No" to skip this step.

Please note the following:

- During the client's execution, you will have the option to request help on how to use the program. The help message provides step-by-step instructions on creating dictionaries, saving files, and sending them to the server.

- Encryption is optional and can be chosen for values in dictionaries. The substitution cipher used is a simple character substitution, and for real-world applications, more secure encryption methods should be used.

- Upon receiving the file on the server, the server will save the file in the "received_files" directory. If the directory does not exist, the server will create it.

- Both the server and client applications are designed to run on the same machine for local testing. If you want to connect the client to a remote server, ensure that you update the `server` variable in the client application to the appropriate server IP address or hostname.

By following these instructions, you can effectively use the Substitution Cipher Server-Client Application for secure transfer and management of dictionaries. Enjoy using the application!

