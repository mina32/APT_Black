from __future__ import print_function
from twisted.internet import reactor, protocol
import sys


# a client protocol
class DemoClient(protocol.Protocol):

    def connectionMade(self):
        data = input('Connection established. Ask the Magic 8 ball a question: ')
        self.transport.write(bytes(data, 'utf-8'))

    def dataReceived(self, data):
        print("Server said:", data.decode('utf-8'))
        ans = input('Would you like to ask another question? Y/N: ')
        if "Y" in ans:
            self.connectionMade()
        else:
            self.transport.loseConnection()

    def connectionLost(self, reason):
        print("No longer connected to the server.")
        reactor.stop()








