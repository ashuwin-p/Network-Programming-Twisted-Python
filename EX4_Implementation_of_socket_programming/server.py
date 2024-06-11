import socket

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8000

    # Bind to the port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen()

    print("Server listening on {}:{}".format(host, port))

    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()

        print("Connection from", addr)

        # Send a message to the client
        message = input(f"Enter Message to {addr} : ")
        client_socket.send(message.encode())

        # Receive data from the client
        data = client_socket.recv(1024)
        print("Received from client:", data.decode())

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    main()
