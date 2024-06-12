from twisted.internet import protocol, reactor
import threading


class Client(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.name = input("Enter name: ")
        self.factory.client = self
        self.transport.write(self.name.encode())
        threading.Thread(target=self.readInput).start()

    def dataReceived(self, data):
        print(data.decode())

    def readInput(self):
        while True:
            msg = input("Enter message to server or 'exit': ")
            if msg == "exit":
                reactor.callFromThread(self.transport.loseConnection)
                break
            reactor.callFromThread(self.transport.write, msg.encode())


class ClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.client = None

    def startedConnecting(self, connector):
        print("Connecting...")

    def buildProtocol(self, addr):
        return Client(self)

    def clientConnectionLost(self, connector, reason):
        print("Disconnected due to", reason)
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed due to", reason)
        reactor.stop()


if __name__ == "__main__":
    factory = ClientFactory()
    reactor.connectTCP("localhost", 8080, factory)
    reactor.run()
