class Request_Packet:
    def __init__(
        self,
        srcMAC,
        srcIP,
        destIP,
        hardwareType="01",
        protocolType="800",
        hardwareLen="06",
        protocolLen="04",
    ):
        self.hardwareType = hardwareType
        self.protocolType = protocolType
        self.hardwareLen = hardwareLen
        self.protocolLen = protocolLen
        self.packetType = 1
        self.srcMAC = srcMAC
        self.srcIP = srcIP
        self.destIP = destIP
        self.destMAC = "00000000"

    def __str__(self):
        representation = ""
        representation += f"Hardware Type                   : {self.hardwareType}\n"
        representation += f"Hardware Length                 : {self.hardwareLen}\n"
        representation += f"Protocol Type                   : {self.protocolType}\n"
        representation += f"Protocol Length                 : {self.protocolLen}\n"
        representation += f"Packet Type                     : {self.packetType}\n"
        representation += f"Source Hardware Address         : {self.srcMAC}\n"
        representation += f"Source IP Address               : {self.srcIP}\n"
        representation += f"Destination Hardware Address    : {self.destMAC}\n"
        representation += f"Destination IP Address          : {self.destIP}"

        return representation


class Reply_Packet:
    def __init__(
        self,
        srcMAC,
        srcIP,
        destMAC,
        destIP,
        hardwareType="01",
        protocolType="800",
        hardwareLen="06",
        protocolLen="04",
    ):
        self.hardwareType = hardwareType
        self.protocolType = protocolType
        self.hardwareLen = hardwareLen
        self.protocolLen = protocolLen
        self.packetType = 2
        self.srcMAC = srcMAC
        self.srcIP = srcIP
        self.destIP = destIP
        self.destMAC = destMAC

    def __str__(self):
        representation = ""
        representation += f"Hardware Type                   : {self.hardwareType}\n"
        representation += f"Hardware Length                 : {self.hardwareLen}\n"
        representation += f"Protocol Type                   : {self.protocolType}\n"
        representation += f"Protocol Length                 : {self.protocolLen}\n"
        representation += f"Packet Type                     : {self.packetType}\n"
        representation += f"Source Hardware Address         : {self.srcMAC}\n"
        representation += f"Source IP Address               : {self.srcIP}\n"
        representation += f"Destination Hardware Address    : {self.destMAC}\n"
        representation += f"Destination IP Address          : {self.destIP}"

        return representation
