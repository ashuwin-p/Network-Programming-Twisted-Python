from twisted.internet import protocol, reactor

class StarProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory  # factory that stores all the clients connected to the server
        self.name = None  # name of the client that will connect to the server

    def connectionMade(self):
        '''establishing a connection to the server'''
        print('New client connected: ')
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Client disconnected")
        self.factory.removeClient(self)

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(self.name, ' has connected to the server.')
        else:
            if message.startswith('@'):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                for client in self.factory.clients:
                    if client!=self:
                        client.transport.write(f"{self.name}:{message}".encode())

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return StarProtocol(self)

    def removeClient(self, client):
        self.clients.remove(client)

if __name__ == "__main__":
    reactor.listenTCP(8080, StarFactory())
    print("Server started. Listening on port 8080...")
    print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
    reactor.run()
















# import subprocess
# from twisted.internet import reactor,defer

# class PingProtocol:
#     def _init_(self):
#         self.deferred = defer.Deferred()

#     def ping(self,host):
#         process = subprocess.Popen(['ping','-c','4',host],stdout = subprocess.PIPE)
#         output,error = process.communicate()
#         if error:
#             self.deferred.errback(error)
#         else:
#             self.deferred.callback(output)

# def print_result(result):
#     print(result.decode())

# def print_error(failure):
#     print(failure)

# if __name__ == '_main_':
#     protocol = PingProtocol()
#     protocol.ping('google.com')
#     protocol.deferred.addCallbacks(print_result,print_error)
#     reactor.run()





# import subprocess
# from twisted.internet import defer,reactor

# class TracerouteCmd:
#     def _init_(self):
#         self.deferred = defer.Deferred()

#     def traceroute(self,host):
#         process = subprocess.Popen(['traceroute','-m','10',host],stdout=subprocess.PIPE)

#         output,error = process.communicate()

#         if error:
#             self.deferred.errback(error)
#         else:
#             self.deferred.callback(output)

# def print_result(result):
#     print(result.decode())

# def print_error(failure):
#     print(failure)

# protocol = TracerouteCmd()
# protocol.traceroute('google.com')
# protocol.deferred.addCallbacks(print_result,print_error)
# reactor.run()