from twisted.internet import protocol, reactor

class EchoServer(protocol.DatagramProtocol):

    def datagramReceived(self, datagram, addr):
        msg = datagram.decode()
        print(f"Message from Client {addr}: {msg}")
        ack_msg = f"ACK: [{msg}]"
        print("Sending Acknowledgement\n")
        self.transport.write(ack_msg.encode(), addr)

if __name__ == '__main__':
    reactor.listenUDP(8000, EchoServer())
    print("Server started listening on port 8000")
    reactor.run()
