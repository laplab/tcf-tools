import tcf
from tcf.util.sync import CommandControl

def connect():
    tcf.protocol.startEventQueue()
    return CommandControl(tcf.connect('TCP:172.16.0.254:1534'))

def unwrap(response):
    error, result = response
    if error:
        print('Error: ', error)
        sys.exit(1)
    return result