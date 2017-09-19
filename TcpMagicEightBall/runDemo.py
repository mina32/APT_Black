from twisted.internet import reactor, protocol, ssl, interfaces
from twistedDemoClient import DemoClient
from twistedDemoServer import MagicEightBall
import sys


#start Server
server = protocol.ServerFactory()
server.protocol = MagicEightBall


#Start client 
client = protocol.ClientFactory()
client.protocol = DemoClient


### TCP Demo
print("Setting up TCP connection...")
reactor.listenTCP(8006, server)
reactor.connectTCP("localhost", 8006, client)

reactor.run()


