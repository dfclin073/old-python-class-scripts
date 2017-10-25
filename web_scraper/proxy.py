#!/usr/bin/python
from twisted.web import proxy, http
from twisted.internet import reactor, protocol

def main():

    class Echo(protocol.Protocol):
        def dataReceived(self, data):
            self.transport.write(data)

    class EchoFactory(protocol.Factory):
        def buildProtocol(self, addr):
            return Echo()
    reactor.listenTCP(8080, EchoFactory())
    reactor.run()

if __name__ == "__main__":
    main()
