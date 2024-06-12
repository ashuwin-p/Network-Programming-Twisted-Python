from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver


class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        self.sendLine(b"Hi, Welcome to the Chat Application !!! ")
        self.sendLine(b"What is your Name ? ")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]

            msg = f"\t\t\t {self.name} has left the Channel "

            print(f"<== {self.name} has left the Channel")

            self.broadcastMessage(msg.encode())

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        name = name.decode()
        if name in self.factory.users:
            self.sendLine(b"Name already Taken :-(")
            return
        print(f"==> {name} has joined the channel")

        msg = f"Welcome {name}, Now you can send messages."
        self.sendLine(msg.encode())

        msg = f"\t\t\t {name} has joined the channel !!"
        self.broadcastMessage(msg.encode())

        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, msg):
        if msg.decode() == "/leave":
            self.transport.loseConnection()
            return

        msg = f"<{self.name}>: {msg.decode()}"
        print("Messaging : ", msg)
        self.broadcastMessage(msg.encode())

    def broadcastMessage(self, msg):
        for name, protocol in self.factory.users.items():
            if protocol != self:  # Broadcast message except for the same user
                protocol.sendLine(msg)


class ChatFactory(protocol.Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


if __name__ == "__main__":
    reactor.listenTCP(8000, ChatFactory())
    reactor.run()
