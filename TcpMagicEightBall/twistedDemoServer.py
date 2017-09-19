from twisted.internet import reactor, protocol
import random

class MagicEightBall(protocol.Protocol):
    def dataReceived(self, data):
        # This server simulates a magic 8 ball
        if "?" in str(data):
            responses = [
                    "It is certain",
                    "Without a doubt",
                    "Most likely",
                    "Yes",
                    "Reply hazy try again",
                    "Ask again later",
                    "Don't count on it",
                    "Very doubtful",     
                    "My sources say no"
            ]
            response = responses[random.randrange(0,9)]
            self.transport.write(bytes(response, 'utf-8'))
        else:
            self.transport.write(bytes("Response is not a question. Please ask a question including a question mark (?).", 'utf-8'))


