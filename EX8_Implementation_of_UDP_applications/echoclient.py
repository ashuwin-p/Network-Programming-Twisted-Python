from twisted.internet import protocol, reactor
import time

class EchoClient(protocol.DatagramProtocol):

    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8000)
        self.sendDatagram()

    def sendDatagram(self):
        message = input("\nEnter Message (or '/exit' to exit): ")
        if message.lower() == '/exit':
            reactor.callLater(0, reactor.stop)
            return

        self.start_time = time.time()
        self.transport.write(message.encode())

    def datagramReceived(self, datagram, host):
        self.end_time = time.time()
        rtt = self.end_time - self.start_time
        print(f"\nAcknowledgement from Server {host} : ")
        print(datagram.decode(), f'<RTT : {rtt}s>', '\n')
        self.sendDatagram()

if __name__ == '__main__':
    reactor.listenUDP(0, EchoClient())
    reactor.run()
