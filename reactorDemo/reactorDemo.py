import time,sys, random
from twisted.internet import reactor

# Use this to log actions to stdout
from twisted.python import log
log.startLogging(sys.stdout)
 
##############################
# Demo of writing to log
##############################
def log_some_stuff(x):
    log.msg(str(x))
reactor.callWhenRunning(log_some_stuff, "Some important thing that should be logged")



##############################
# Demo of delaying a function call
##############################
now = time.localtime(time.time())
log.msg("It is currently: " + str(time.strftime("%y/%m/%d %H:%M:%S",now)))
reactor.callLater(2, log_some_stuff, "It should be 2 sec later...")


##############################
#Demo of firing system events
##############################
def handle_special_event():
    log_some_stuff("A special event was triggered.")

reactor.callLater(4, reactor.fireSystemEvent, 'SpecialEventName')
reactor.addSystemEventTrigger('during', 'SpecialEventName', handle_special_event)


reactor.run()
