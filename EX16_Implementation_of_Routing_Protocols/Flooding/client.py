from twisted.internet import protocol, reactor
import json


class FloodClient(protocol.Protocol):
    def connectionMade(self):
        graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["E"], "D": ["A"], "E": []}
        print("The graph is:", graph)
        source = input("Enter start vertex for flooding: ")
        msg = input("Enter message: ")
        data = {"graph": graph, "start": source, "msg": msg}
        self.transport.write(json.dumps(data).encode())
        self.transport.loseConnection()


class FloodClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return FloodClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection Failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        reactor.stop()


reactor.connectTCP("localhost", 8000, FloodClientFactory())
reactor.run()
