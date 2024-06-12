from twisted.internet import reactor, protocol


class DropLink(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected to bus backbone.")

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected.")

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(f"{self.name} connected to bus.")
        else:
            if message.startswith("@"):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
            else:
                self.transport.write(f"Error: User {recipient} not found.\n".encode())

    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client != self:
                client.transport.write(f"{message}\n".encode())


class BusBackbone(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return DropLink(self)


if __name__ == "__main__":
    reactor.listenTCP(8080, BusBackbone())
    print("Bus server started.")
    print(
        "Enter your name as first message to register. To send a message to a particular username use '@username: message'."
    )
    reactor.run()


# from twisted.internet import protocol,reactor

# class Droplink(protocol.Protocol):
#     def __init__(self,factory):
#         self.factory=factory
#         self.name=None

#     def connection_made(self):
#         self.factory.clients.append(self)
#         print("Connection was made")

#     def connection_lost(self):
#         self.factory.clients.remove(self)
#         print("Connection was lost")

#     def data_received(self,message):
#         data=message.decode().strip
#         if self.name is None:
#             self.name=data
#         else:
#             if data.startswith('@'):
#                 recepient,private_message=data[1:].strip(':',1)
#                 self.sendPrivatemessage(recepient,private_message)
#             else:
#                 self.sendBroadcastmessage(message)
#                 print("Sender:",self.name,"\nMessage:",message)

#     def sendPrivatemessage(self,recipient,message):
#         for client in self.factory.clients:
#             if client.name==recipient:
#                 self.transport.write(f"(Private) {self.name}:{message}".encode())
#             else:
#                 self.transport.write(f"user not found")

#     def sendBroadcastmessage(self,message):
#         for client in self.factory.clients:
#             if client!=self:
#                 client.transport.write(f"{message}\n".encode())

# class BusBackbone(protocol.Factory):
#     def __init__(self):
#         self.clients=[]

#     def buildProtocol(self):
#         return Droplink(self)

# if __name__ == "__main__":
#     reactor.listenTCP(8080, BusBackbone())
#     print("Bus server started.")
#     print("Enter your name as first message to register. To send a message to a particular username use '@username: message'.")
#     reactor.run()


# from twisted.internet import reactor,protocol

# class Serverclass(protocol.Protocol):
#     def __init__(self,factory):
#         self.factory=factory
#         self.name=None

#     def connectionMade(self):
#         self.factory.clients.append(self)
#         print("New Connection made")

#     def connectionLost(self, reason):
#         self.factory.clients.remove(self)
#         print("Connection was lost due to",reason)

#     def dataReceived(self, data):
#         msg=data.decode()
#         if self.name is None:
#             self.name=msg
#             print("Name:",self.name)
#         else:
#             if msg.startswith('@'):
#                 receiver,message=msg[1:].split(':',1)
#                 self.private(receiver,message)
#             else:
#                 print(f"{self.name}:{msg}")
#                 self.broadcast(f"{self.name}:{msg}")

#     def private(self,receiver,message):
#         for client in self.factory.clients:
#             if client.name==receiver:
#                 client.transport.write(f"{self.name}:{message}".encode())

#     def broadcast(self,message):
#         for client in self.factory.clients:
#             if client!=self:
#                 client.transport.write(message.encode())

# class ChatFactory(protocol.Factory):
#     def __init__(self):
#         self.clients=[]

#     def buildProtocol(self,addr):
#         return Serverclass(self)

# if __name__=="__main__":
#     reactor.listenTCP(8080,ChatFactory())
#     print("Bus server ready")
#     reactor.run()
