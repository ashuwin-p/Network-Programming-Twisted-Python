from twisted.spread import pb
from twisted.internet import protocol, reactor


class Arithmetic(pb.Root):
    def remote_add(self, n1, n2):
        print("\nProcessing ...")
        answer = n1 + n2
        print(f"Addition Result {n1} + {n2} = {answer}")
        return answer

    def remote_sub(self, n1, n2):
        print("\nProcessing ...")
        answer = n1 - n2
        print(f"Subtraction Result {n1} - {n2} = {answer}")
        return answer

    def remote_mul(self, n1, n2):
        print("\nProcessing ...")
        answer = n1 * n2
        print(f"Multiplication Result {n1} * {n2} = {answer}")
        return answer

    def remote_div(self, n1, n2):
        print("\nProcessing ...")
        answer = n1 / n2
        print(f"Division Result {n1} / {n2} = {answer}")
        return answer


if __name__ == "__main__":
    service = Arithmetic()
    factory = pb.PBServerFactory(service)
    reactor.listenTCP(8000, factory)
    reactor.run()
