from twisted.internet import reactor, protocol
import json


class FloodServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")

    def dataReceived(self, data):
        recv = json.loads(data.decode())
        graph = recv.get("graph")
        start = recv.get("start")
        msg = recv.get("msg")
        self.flood(graph, start, msg)

    def flood(self, graph, source, msg):
        print("Flooding the message")
        visited = set()
        to_visit = [(source, None)]  # (current_node, incoming_link)

        while to_visit:
            current_node, incoming_link = to_visit.pop(0)
            if current_node not in visited:
                visited.add(current_node)
                for neighbor in graph.get(current_node, []):
                    if neighbor != incoming_link and neighbor not in visited:
                        print(f"Message sent from {current_node} to {neighbor}: {msg}")
                        to_visit.append((neighbor, current_node))



class FloodFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return FloodServer()


if __name__ == "__main__":
    reactor.listenTCP(8000, FloodFactory())
    reactor.run()
