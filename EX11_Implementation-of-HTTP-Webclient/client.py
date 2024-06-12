from twisted.internet import reactor, protocol
from twisted.web.client import Agent
import webbrowser


class ResponsePrinter(protocol.Protocol):
    def __init__(self):
        self.content = b""

    def dataReceived(self, data):
        self.content += data

    def connectionLost(self, reason):
        with open("output.html", "wb") as f:
            f.write(self.content)
        print("Output saved to 'output.html'")
        webbrowser.open("output.html")
        reactor.stop()


def got_response(response):
    response.deliverBody(ResponsePrinter())


agent = Agent(reactor)
inpurl = str(input("Enter the URL - "))
url = f"http://localhost:8000?url=http://{inpurl}"
d = agent.request(b"GET", url.encode())
d.addCallback(got_response)
reactor.run()
