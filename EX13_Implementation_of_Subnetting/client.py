from twisted.internet import protocol, reactor
import json


class SubnetClientProtocol(protocol.Protocol):
    def connectionMade(self):
        ip = input("Enter IP address: ")
        subnet_mask = input("Enter subnet mask: ")
        self.transport.write(f"{ip},{subnet_mask}".encode())

    def dataReceived(self, data):
        response = json.loads(data.decode())
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print(f"Number of subnets: {response['num_subnets']}")
            print("Subnets:")
            for subnet in response["subnets"]:
                print(subnet)
            print(f"Number of hosts per subnet: {response['num_hosts']}")
            print("Host addresses:")
            for host in response["hosts"]:
                print(host)

        self.transport.loseConnection()


class SubnetClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return SubnetClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()


def main():
    reactor.connectTCP("localhost", 8000, SubnetClientFactory())
    reactor.run()


if __name__ == "__main__":
    main()
