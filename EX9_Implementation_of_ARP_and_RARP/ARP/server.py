# server.py
from twisted.internet import protocol, reactor
import pickle
from packets import Request_Packet, Reply_Packet

global arp_table


class ARPServer(protocol.Protocol):
    def dataReceived(self, data):
        request_packet = pickle.loads(data)
        print("\n\nARP Request Packet \n\n", request_packet)
        IP = request_packet.destIP
        if IP not in arp_table:
            self.transport.write(b"NOT FOUND")
        else:
            MAC = arp_table[IP]
            reply_packet = Reply_Packet(
                MAC, IP, request_packet.srcMAC, request_packet.srcIP
            )
            print("\n\nARP Reply Packet \n\n", reply_packet)
            data = pickle.dumps(reply_packet)
            print("\n>>>>>>>>>>>> Sending ARP Reply Packet")
            self.transport.write(data)


class ARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ARPServer()


arp_table = {}
arp_table["130.23.43.24"] = "A4:6E:F4:59:83:AC"
arp_table["130.23.43.25"] = "A4:6E:F4:59:83:AB"
arp_table["130.23.43.26"] = "A4:6E:F4:59:83:DB"

if __name__ == "__main__":
    reactor.listenTCP(8000, ARPServerFactory())
    reactor.run()
