from twisted.internet import reactor, protocol


class SNMPClient(protocol.DatagramProtocol):

    def startProtocol(self):
        print("Connecting to SNMP Agent")
        self.transport.connect("127.0.0.1", 8000)
        self.send_request()

    def send_request(self):
        # Send the request message here
        request = "[Request] : Request from SNMP Manager"
        self.transport.write(request.encode())
        print("Request sent")

    def datagramReceived(self, data, addr):
        print(data.decode())
        reactor.stop()


reactor.listenUDP(0, SNMPClient())
reactor.run()
