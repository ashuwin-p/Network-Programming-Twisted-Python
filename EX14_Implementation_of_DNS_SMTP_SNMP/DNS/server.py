from twisted.internet import reactor, protocol

global dns_table


class DNS_Server(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")

    def dataReceived(self, data):
        domain_name = data.decode()
        if domain_name in dns_table:
            ip = dns_table[domain_name]
            msg = domain_name + " => " + ip
            self.transport.write(msg.encode())
            print(f"IP address for {domain_name} sent to client")
        else:
            self.transport.write(b"None")
            print(f"IP address for {domain_name} Unavailable")


class DNS_Server_Factory(protocol.Factory):
    def buildProtocol(self, addr):
        return DNS_Server()


dns_table = {}
dns_table["www.google.com"] = "156.3.20.4"
dns_table["www.youtube.com"] = "156.7.10.4"
dns_table["www.gmail.com"] = "157.7.20.3"
dns_table["www.ssn.edu.in"] = "192.168.20.3"

reactor.listenTCP(8000, DNS_Server_Factory())
reactor.run()
