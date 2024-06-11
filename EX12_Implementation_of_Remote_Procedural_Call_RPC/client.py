from twisted.spread import pb
from twisted.internet import reactor


# Callback functions to handle results from the server
def add_handle_result(result):
    print("Result of Addition:", result)


def sub_handle_result(result):
    print("Result of subtraction:", result)


def mul_handle_result(result):
    print("Result of multiplication:", result)


def div_handle_result(result):
    print("Result of division:", result)


# Error handling function
def connection_error(err):
    print("Connection error:", err)
    reactor.stop()


# Function to connect to the server and call remote methods
def connect():
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8000, factory)
    d = factory.getRootObject()

    # Chain callbacks to call remote methods in sequence
    d.addCallback(
        lambda obj: obj.callRemote(
            "add", int(input("Enter number1: ")), int(input("Enter number2: "))
        )
    )
    d.addCallback(add_handle_result)

    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "subtract", int(input("Enter number1: ")), int(input("Enter number2: "))
        )
    )
    d.addCallback(sub_handle_result)

    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "multiply", int(input("Enter number1: ")), int(input("Enter number2: "))
        )
    )
    d.addCallback(mul_handle_result)

    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "divide", int(input("Enter number1: ")), int(input("Enter number2: "))
        )
    )
    d.addCallback(div_handle_result)

    # Handle errors
    d.addErrback(connection_error)


# Run the connect function when the reactor starts
reactor.callWhenRunning(connect)
reactor.run()
