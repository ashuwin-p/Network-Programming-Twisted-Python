from twisted.internet import reactor, protocol

class EchoServer(protocol.Protocol):
    
    def dataReceived(self, data):
        print("Message from Client -", data.decode())
        print("Client Connected!")
        ack_msg = f"{data.decode()}"
        ack =  f" Received { {ack_msg} }"
        print("sending Acknoledgement")
        self.transport.write(ack.encode())
    
class EchoFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return EchoServer()

reactor.listenTCP(8000,EchoFactory())
reactor.run()
