from twisted.internet import protocol, reactor

class StopAndWaitServer(protocol.Protocol):
    def connectionMade(self):
        print("Client Connected")
        self.send_message()

    def send_message(self):
        self.msg = input("Enter Message to client: ")
        self.expected_ack = b"[ACK]"
        self.transport.write(self.msg.encode())
        self.sent_msg = self.msg.encode()
        self.schedule_resend()

    def dataReceived(self, data):
        if data.strip() == self.expected_ack:
            print("Acknowledgement Received\n")
            if hasattr(self, 'resend_call') and self.resend_call.active():
                self.resend_call.cancel()
            self.send_message()
        else:
            print("Unexpected data received:", data)

    def resend_message(self):
        print("Acknowledgement not received")
        print("Resending Last Message...")
        self.transport.write(self.sent_msg)
        self.schedule_resend()

    def schedule_resend(self):
        self.resend_call = reactor.callLater(5, self.resend_message)

    def connectionLost(self, reason):
        print("Client Disconnected")

class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopAndWaitServer()

if __name__ == "__main__":
    reactor.listenTCP(8000, StopAndWaitServerFactory())
    reactor.run()
