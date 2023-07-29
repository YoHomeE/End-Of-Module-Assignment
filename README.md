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

## Unit Tests

These tests are aimed at testing the individual functions within the client-server application across a variety of inputs to ensure each function works as expected without any bugs.

### Client Unit Tests

1. **utest1:**
   Description: Test the function responsible for connecting the client to the server.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 utest1.py
     ```

2. **utest2:**
   Description: Test the encryption and decryption functions for dictionary values using a substitution cipher.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 utest2.py
     ```

3. **utest4:**
   Description: Test the method for creating dictionaries with the specified keys and values.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 utest4.py
     ```

4. **utest5:**
   Description: Test the method for saving files in JSON, Binary, and XML formats.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 utest5.py
     ```

### Server Unit Tests

1. **sutest1:**
   Description: Test the server's file receiving function to ensure files are correctly received and saved in the "received_files" directory.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 sutest1.py
     ```

2. **sutest2:**
   Description: test suite for the Server class. It includes test cases to verify that the server can successfully send and receive data
   with connected clients. The tests evaluate the correctness of the send_data and receive_data methods in handling data transmission.
   Additionally, the suite contains tests for the receive_metadata method, which ensures that the server can receive metadata about files
   from clients and save the files appropriately in JSON, pickle, and XML formats.
   Instructions to run:
   - Navigate to the "tests" folder within the Final Project Code folder.
   - Run the following command:
     ```
     python3 sutest2.py
     ```

Make sure you have the necessary environment set up before running the unit tests. The tests will provide valuable insights into the functionality and correctness of the client-server application. Enjoy testing!


