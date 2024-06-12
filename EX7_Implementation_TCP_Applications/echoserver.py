from twisted.internet import reactor, protocol


class EchoServer(protocol.Protocol):
    def connectionMade(self):
        peer = self.transport.getPeer()
        print(f"Connection established with {peer}")

    def connectionLost(self, reason):
        print(f"Connection lost: {reason}")

    def dataReceived(self, data):
        message = data.decode()
        print(f"Message from Client: {message}")
        ack = f"[ACK]: {message}"
        self.transport.write(ack.encode())
        print("Acknowledgement sent")


class EchoServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoServer()


def main():
    PORT = 8000
    FACTORY = EchoServerFactory()
    reactor.listenTCP(PORT, FACTORY)
    print(f"Server Started on port {PORT}")
    reactor.run()


if __name__ == "__main__":
    main()
