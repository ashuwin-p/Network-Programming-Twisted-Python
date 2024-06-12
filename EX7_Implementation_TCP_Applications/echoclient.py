from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to Server")
        self.send_message()

    def send_message(self):
        print("Type '..quit' to exit")
        msg = input("Enter Message: ")
        if msg == "..quit":
            self.transport.loseConnection()
        else:
            self.transport.write(msg.encode())

    def dataReceived(self, data):
        print("Acknowledgement Received from server:", data.decode())
        self.send_message()


class EchoClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionLost(self, connector, reason):
        print("Connection Lost:", reason)
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Connection Failed:", reason)
        reactor.stop()


def main():
    SERVER_ADDRESS = "localhost"
    SERVER_PORT = 8000
    CLIENT_FACTORY = EchoClientFactory()
    reactor.connectTCP(SERVER_ADDRESS, SERVER_PORT, CLIENT_FACTORY)
    reactor.run()


if __name__ == "__main__":
    main()
