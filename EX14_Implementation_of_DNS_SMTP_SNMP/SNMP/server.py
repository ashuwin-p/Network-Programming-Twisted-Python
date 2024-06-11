from twisted.internet import protocol, reactor


class SNMPServer(protocol.DatagramProtocol):
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode()
        # Process the request here
        response = f"[Response]: Response from SNMP Agent"
        self.transport.write(response.encode(), addr)
        print("Response Sent")


reactor.listenUDP(8000, SNMPServer())
reactor.run()
