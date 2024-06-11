import subprocess
from twisted.internet import reactor, defer, threads


class TracerouteCmd:
    def __init__(self):
        self.deferred = defer.Deferred()

    def traceroute(self, host):
        def run_traceroute():
            process = subprocess.Popen(
                ["traceroute", "-m", "10", host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output, error = process.communicate()
            if process.returncode != 0:
                raise Exception(error.decode())
            return output

        d = threads.deferToThread(run_traceroute)
        d.addCallback(self.deferred.callback)
        d.addErrback(self.deferred.errback)


def print_result(result):
    print(result.decode())
    reactor.stop()


def print_error(failure):
    print(failure)
    reactor.stop()


protocol = TracerouteCmd()
protocol.traceroute("google.com")
protocol.deferred.addCallbacks(print_result, print_error)

reactor.run()
