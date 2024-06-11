from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class DistanceVectorRoutingProtocol(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routing_table = {}
        self.neighbor_routers = []

    def startProtocol(self):
        self.transport.joinGroup("224.0.0.0")
        print(f"Started routing protocol on {self.host}:{self.port}")
        if self.port == 8000:
            self.updateRoutingTable("A", "A", 0)
            self.sendRoutingUpdate("A", "B", 2)
            self.sendRoutingUpdate("A", "C", 4)
            self.sendRoutingUpdate("A", "D", 7)

    def sendRoutingUpdate(self, source, destination, cost):
        routing_update = f"{source},{destination},{cost}"
        self.transport.write(routing_update.encode(), ("224.0.0.0", self.port))

    def datagramReceived(self, datagram, address):
        routing_update = datagram.decode()
        source, destination, cost = routing_update.split(",")
        self.updateRoutingTable(source, destination, int(cost))
        print(f"Received routing update from {address}: {routing_update}")

    def updateRoutingTable(self, source, destination, cost):
        if (
            destination not in self.routing_table
            or cost < self.routing_table[destination][1]
        ):
            self.routing_table[destination] = (source, cost)

    def calculateShortestPaths(self):
        infinity = float("inf")
        shortest_paths = {
            router: (infinity, None) for router in self.routing_table.keys()
        }
        shortest_paths[self.host] = (0, self.host)

        updated = True
        while updated:
            updated = False
            for neighbor, (nh, cost) in self.routing_table.items():
                for dest, (nh_dest, cost_dest) in self.routing_table.items():
                    if neighbor != self.host and dest != self.host:
                        new_cost = cost + cost_dest
                        if new_cost < shortest_paths[dest][0]:
                            shortest_paths[dest] = (new_cost, neighbor)
                            updated = True

        self.routing_table = {
            dest: (nh_dest, cost_dest)
            for dest, (cost_dest, nh_dest) in shortest_paths.items()
        }
        print("Routing table updated:")
        print("Destination Next Hop Cost")
        for dest, (nh, cost) in self.routing_table.items():
            print(f"{dest}\t\t{nh}\t\t{cost}")

        self.broadcastRoutingTable()

    def broadcastRoutingTable(self):
        print("Broadcasting routing table:")
        for dest, (nh, cost) in self.routing_table.items():
            routing_update = f"{self.host},{dest},{cost}"
            self.transport.write(routing_update.encode(), ("224.0.0.0", self.port))


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    protocol = DistanceVectorRoutingProtocol(host, port)
    reactor.listenMulticast(port, protocol, listenMultiple=True)
    reactor.callLater(5, protocol.calculateShortestPaths)
    reactor.run()
