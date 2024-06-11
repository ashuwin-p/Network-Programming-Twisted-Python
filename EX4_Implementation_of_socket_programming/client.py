import socket

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8000

    # Connect to the server
    client_socket.connect((host, port))

    # Receive the message from the server
    data = client_socket.recv(1024)
    print("Received from server:", data.decode())

    # Send a message to the server
    message = input("Enter Message to Server : ")
    client_socket.send(message.encode())

    

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()
