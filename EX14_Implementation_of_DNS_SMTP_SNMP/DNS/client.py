from twisted.internet import reactor, protocol


class DNS_Client(protocol.Protocol):
    def connectionMade(self):
        print("Connected to DNS server")
        domain_name = input("Enter Domain Name - ")
        self.transport.write(domain_name.encode())

    def dataReceived(self, data):
        if data == b"None":
            print("IP for Domain Name couldn't be resolved")

        else:
            ip = data.decode()
            print(ip)
        self.transport.loseConnection()


class DNS_Client_Factory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return DNS_Client()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("connection lost")
        reactor.stop()


reactor.connectTCP("localhost", 8000, DNS_Client_Factory())
reactor.run()
