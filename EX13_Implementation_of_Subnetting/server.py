from twisted.internet import protocol, reactor
import ipaddress
import json


class SubnetServerProtocol(protocol.Protocol):
    def dataReceived(self, data):
        try:
            ip, subnet_mask = data.decode().strip().split(",")
            network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)

            # Generate host and subnet information
            hosts = [str(host) for host in network.hosts()]
            subnets = [str(subnet) for subnet in network.subnets()]

            # Determine the number of subnets and hosts per subnet using len()
            num_subnets = len(subnets)
            num_hosts = len(hosts)

            response = json.dumps(
                {
                    "num_subnets": num_subnets,
                    "num_hosts": num_hosts,
                    "hosts": hosts,
                    "subnets": subnets,
                }
            )
        except ValueError as e:
            response = json.dumps({"error": str(e)})

        self.transport.write(response.encode())
        self.transport.loseConnection()


class SubnetServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SubnetServerProtocol()


reactor.listenTCP(8000, SubnetServerFactory())
reactor.run()
