from twisted.internet import protocol, reactor
import time

class FTP_Server(protocol.Protocol):
    def connectionMade(self):
        print("Client Connected \n")

    def dataReceived(self, data):
        if data == b'REQUEST TO SEND':
            self.transport.write(b'READY TO RECEIVE')
            self.file_transfer = True
            self.start_time = time.time()

        elif self.file_transfer:
            file = open('received.txt','wb')
            file.write(data)
            file.close()
            self.end_time = time.time()
            self.transport.write(b'FILE RECEIVED')
            print('\n',"="*30)
            print("File Received")
            print("Round Trip Time : ", self.end_time - self.start_time)
            print('\n',"="*30)

class FTP_Server_Factory(protocol.ServerFactory):
    def buildProtocol(self, addr):
        return FTP_Server()
    
if __name__ == "__main__":
    reactor.listenTCP(7000, FTP_Server_Factory())
    print("Server started.")
    reactor.run()