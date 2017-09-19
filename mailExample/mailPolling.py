import os
from twisted.internet import reactor, defer

def read_mail(mailitems):
    print(mailitems)
    return "Junk Mail... Sending to shredder: " + mailitems

def shred_mail(mailitems):
    print('buzzzzz: ' + mailitems)
    os.remove('mail')
    reactor.stop()

def create_mail(msg):
    with open("mail","w") as f:
        f.write(msg)

def wait_for_mail(d=None):
    if not d:
        d = defer.Deferred()
    if not os.path.isfile('mail'):
        reactor.callLater(1, wait_for_mail, d)
    else:
        with open("mail") as f:
            contents = f.readlines()
        d.callback(contents[0])
    return d

deferred = wait_for_mail()
deferred.addCallback(read_mail)
deferred.addCallback(shred_mail)
reactor.callLater(2, create_mail, "Look at this new letter!")
reactor.callLater(20, reactor.stop)
reactor.run()


