from twisted.spread import pb
from twisted.internet import reactor


# Define a class that inherits from pb.Root to create a remote service
class MyService(pb.Root):
    # Define the remote methods that can be called by the clients
    def remote_add(self, x, y):
        print("ADDITION:\n", x + y)
        return x + y

    def remote_subtract(self, x, y):
        print("SUBTRACTION:\n", x - y)
        return x - y

    def remote_multiply(self, x, y):
        print("MULTIPLICATION:\n", x * y)
        return x * y

    def remote_divide(self, x, y):
        if y != 0:
            print("DIVISION:\n", x / y)
            return x / y
        else:
            raise ValueError("Cannot divide by zero.")


# Create an instance of the service
service = MyService()
# Create a PBServerFactory with the service instance
factory = pb.PBServerFactory(service)

reactor.listenTCP(8000, factory)
reactor.run()
