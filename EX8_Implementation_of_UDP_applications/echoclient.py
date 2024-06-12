from twisted.internet import protocol, reactor


class EchoClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect(SERVER_HOST, SERVER_PORT)
        print("Connected to Server")
        self.sendDatagram()

    def sendDatagram(self):
        print(">quit to quit the application")
        datagram = input("Enter Data - ")
        if datagram == ">quit":
            reactor.callLater(0, reactor.stop)
            return
        self.transport.write(datagram.encode())

    def datagramReceived(self, datagram, host):
        print("Server : ", datagram.decode())
        self.sendDatagram()


def run_client():
    reactor.listenUDP(0, EchoClient())
    reactor.run()


if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8000
    run_client()
