from twisted.internet import protocol, reactor


class EchoServer(protocol.DatagramProtocol):
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode()
        print("Client : ", datagram)
        ack = "[ACK] :" + datagram
        self.transport.write(ack.encode(), addr)


def run_server():
    reactor.listenUDP(SERVER_PORT, EchoServer())
    print(f"Server listening on port {SERVER_PORT}")
    reactor.run()


if __name__ == "__main__":
    SERVER_PORT = 8000
    run_server()
