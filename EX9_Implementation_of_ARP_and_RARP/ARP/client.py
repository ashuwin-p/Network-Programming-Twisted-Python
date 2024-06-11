from twisted.internet import reactor, protocol
import struct


class ARPClient(protocol.Protocol):

    def connectionMade(self):
        arp_packet_format = "!6s4s6s4s"
        request_packet = struct.pack(
            arp_packet_format,
            bytes([00, 11, 22, 33, 44, 55]),  # Example source hardware address
            bytes([0, 0, 0, 0]),  # Example source protocol address
            bytes([17, 18, 19, 20, 21, 22]),  # Example target hardware address
            bytes([26, 27, 28, 29]),  # Example target protocol address
        )

        a = input("enter IP address:")
        to_serv = {
            "ip": a,
            "req_format": request_packet,
            "req": "ARP_REQUEST",
        }  # dict is used
        self.transport.write(str(to_serv).encode())

    def dataReceived(self, data):
        recv = eval(data.decode())  # data is decoded with same structure sent(dict)
        arp_packet_format = "!6s4s6s4s"
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address,
        ) = struct.unpack(
            arp_packet_format, recv.get("reply_format")
        )  # unpacking the format

        print("Received ARP reply:")
        print(
            "Source Hardware Address:",
            ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address),
        )
        print(
            "Source Protocol Address:",
            ".".join(str(byte) for byte in Source_Protocol_Address),
        )
        print(
            "Target Hardware Address:",
            ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address),
        )
        print(
            "Target Protocol Address:",
            ".".join(str(byte) for byte in Target_Protocol_Address),
        )

        if recv.get("data").startswith("ARP_REPLY"):

            reply_parts = recv.get("data").split()
            if len(reply_parts) == 3:

                mac_address = reply_parts[2]
                ip_address = reply_parts[1]
                print(f"Received ARP reply: IP = {ip_address }, MAC = {mac_address}")
                self.transport.loseConnection()  # to terminate after the data is print
            else:
                print("Invalid ARP reply")
                self.transport.loseConnection()
        else:
            print("invalid IP Address given !!!")
            self.transport.loseConnection()


class ARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ARPClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()


reactor.connectTCP("localhost", 1234, ARPClientFactory())
reactor.run()
