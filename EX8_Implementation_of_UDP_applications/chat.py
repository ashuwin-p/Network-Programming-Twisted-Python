from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class ChatServer(DatagramProtocol):
    def __init__(self):
        self.users = {}  # Maps user addresses to usernames

    def connectionMade(self):
        self.transport.write(b"Please enter your username:\n")

    def datagramReceived(self, data, addr):
        message = data.decode()
        if addr not in self.users:
            # If the user is not registered, use the received message as their username
            username = message
            self.users[addr] = username
            self.transport.write(f"Welcome, {username}!\n".encode())
            self.broadcastMessage(f"{username} has joined the chat.\n", addr)
        else:
            # If the user is already registered, broadcast the message to all other users
            username = self.users[addr]
            self.broadcastMessage(f"<{username}> {message}\n", addr)

    def broadcastMessage(self, message, sender_addr):
        for user_addr, username in self.users.items():
            if user_addr != sender_addr:
                self.transport.write(message.encode(), user_addr)

if __name__ == "__main__":
    reactor.listenUDP(8000, ChatServer())
    print("Server started.")
    reactor.run()
