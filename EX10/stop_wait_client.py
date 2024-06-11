from twisted.internet import reactor, protocol

class StopWaitClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to Server")

    def send_ack(self):
        self.transport.write(b"[ACK]")
        print("Acknowledgement sent \n")

    def dataReceived(self, data):
        print("Message received:", data.decode())
        choice = input("Enter 'y' to send acknowledgement: ")
        if choice.lower() == "y":
            self.send_ack()

    def connectionLost(self, reason):
        print("Connection Lost")

class StopWaitClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StopWaitClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection Failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection Lost")
        reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP("localhost", 8000, StopWaitClientFactory())
    reactor.run()
