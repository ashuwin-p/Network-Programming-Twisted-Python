from twisted.internet import protocol, reactor
import time

class FTP_Server(protocol.DatagramProtocol):
    def datagramReceived(self, datagram, addr):
        if datagram == b'REQUEST TO SEND':
            self.transport.write(b'READY TO RECEIVE', addr)
            self.file_transfer = True
            self.start_time = time.time()

        elif self.file_transfer:
            file = open('received.txt','wb')
            file.write(datagram)
            file.close()
            self.end_time = time.time()
            self.transport.write(b'FILE RECEIVED', addr)
            print('\n',"="*30)
            print("File Received")
            print("Round Trip Time : ", self.end_time - self.start_time)
            print('\n',"="*30)

if __name__ == '__main__':
    reactor.listenUDP(8000, FTP_Server())
    print("UDP server started.")
    reactor.run()
