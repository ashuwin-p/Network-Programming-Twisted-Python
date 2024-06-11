from twisted.internet import protocol, reactor
import time

class FTP_Client(protocol.Protocol):
    def connectionMade(self):
        try:
            file = open("sample.txt", 'rb')
            self.file_content = file.read()
            file.close()

            self.transport.write(b'REQUEST TO SEND')

        except FileNotFoundError:
            print("File Not Found !!")
            self.transport.loseConnection()

    def dataReceived(self, data):
        if data == b'READY TO RECEIVE':
            self.start_time = time.time()
            self.transport.write(self.file_content)

        elif data == b'FILE RECEIVED':
            self.end_time = time.time()
            print('\n',"="*30)
            print("File Sent")
            print("Round Trip Time : ", self.end_time - self.start_time)
            print('\n',"="*30)
            self.transport.loseConnection()


class FTP_Client_Factrory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return FTP_Client()
            
if __name__ == "__main__":
    reactor.connectTCP("localhost", 7000, FTP_Client_Factrory())
    reactor.run()
           