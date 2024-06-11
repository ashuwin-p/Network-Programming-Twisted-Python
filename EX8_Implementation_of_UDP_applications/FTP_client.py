from twisted.internet import protocol, reactor
import time

class FTP_client(protocol.DatagramProtocol):

    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8000)
        self.sendDatagram()

    def sendDatagram(self):
        self.start_time = time.time()
        try:
            file = open("sample.txt", 'rb')
            self.file_content = file.read()
            file.close()

            self.transport.write(b'REQUEST TO SEND')

        except FileNotFoundError:
            print("File Not Found !!")
            reactor.stop()

    def datagramReceived(self, datagram, host):
        if datagram == b'READY TO RECEIVE':
            self.transport.write(self.file_content)

        elif datagram == b'FILE RECEIVED':
            self.end_time = time.time()
            print('\n',"="*30)
            print("File Sent")
            print("Round Trip Time : ", self.end_time - self.start_time)
            print('\n',"="*30)
            reactor.stop()

if __name__ == '__main__':
    reactor.listenUDP(0, FTP_client())
    reactor.run()

        