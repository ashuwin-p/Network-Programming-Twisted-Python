# client.py
from twisted.internet import protocol, reactor
import pickle
from packets import Request_Packet, Reply_Packet


class ARPClient(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Connected to Server")
        srcMAC = self.factory.srcMAC
        srcIP = self.factory.srcIP
        destIP = self.factory.destIP
        data = Request_Packet(srcMAC, srcIP, destIP)
        print("\n\nARP REQUEST PACKET \n\n", data)
        request_packet = pickle.dumps(data)
        print("\n >>>>>>>>>>>>>>>>>>> Sending ARP request Packet")
        self.transport.write(request_packet)

    def dataReceived(self, data):
        if data == b"NOT FOUND":
            print("\n\nMAC address not found for given destination IP address")
            self.transport.loseConnection()
        else:
            reply_packet = pickle.loads(data)  # Fixed the assignment
            print("\n\nARP Reply Packet \n\n", reply_packet)
            self.transport.loseConnection()


class ARPClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.srcMAC = "B2:34:55:10:22:10"
        self.srcIP = "130.23.43.20"
        self.destIP = "130.23.43.25"

    def buildProtocol(self, addr):
        return ARPClient(self)

    def clientConnectionLost(self, connector, reason):
        print("\nConnection Closed")
        reactor.stop()


if __name__ == "__main__":
    reactor.connectTCP("localhost", 8000, ARPClientFactory())
    reactor.run()
