from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
	def connectionMade(self):
		print("* * * Connection Made * * * ")
		msg = input("Enter Message to Server : ")
		self.transport.write(msg.encode())
		
		
	def dataReceived(self, data):
		print("Acknowledgement from Server : ", data.decode())
		self.transport.loseConnection()
		
	
class EchoFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return EchoClient()
		
	
	def clientConnectionFailed(self, connector, reason):
		print ("Connection Failed")
		reactor.stop()
		
	def clientConnectionLost(self, connector, reason):
		print ("Connection Lost")
		reactor.stop()
		
	
reactor.connectTCP('localhost',8000, EchoFactory())
reactor.run()
