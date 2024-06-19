from twisted.spread import pb
from twisted.internet import reactor


def handle_add(result):
    print("\nAddition Result : ", result, "\n")


def handle_sub(result):
    print("\nSubtraction Result : ", result, "\n")


def handle_mul(result):
    print("\nMultiplication Result : ", result, "\n")


def handle_div(result):
    print("\nDivision Result : ", result, "\n")


def shutdown(_):
    print("Shutting down reactor.")
    reactor.stop()


def connect():
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8000, factory)

    d = factory.getRootObject()

    # Addition
    d.addCallback(
        lambda obj: obj.callRemote(
            "add",
            eval(input("Enter Number 1 for addition: ")),
            eval(input("Enter Number 2 for addition: ")),
        )
    )
    d.addCallback(handle_add)

    # Subtraction
    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "sub",
            eval(input("Enter Number 1 for subtraction: ")),
            eval(input("Enter Number 2 for subtraction: ")),
        )
    )
    d.addCallback(handle_sub)

    # Multiplication
    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "mul",
            eval(input("Enter Number 1 for multiplication: ")),
            eval(input("Enter Number 2 for multiplication: ")),
        )
    )
    d.addCallback(handle_mul)

    # Division
    d.addCallback(lambda _: factory.getRootObject())
    d.addCallback(
        lambda obj: obj.callRemote(
            "div",
            eval(input("Enter Number 1 for division: ")),
            eval(input("Enter Number 2 for division: ")),
        )
    )
    d.addCallback(handle_div)

    # Shut down the reactor after all operations
    d.addCallback(shutdown)


reactor.callWhenRunning(connect)
reactor.run()
