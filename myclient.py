"""

IRC client exemplar.

"""

from lib2to3.pgen2.token import EQUAL
import sys
from ex2utils import Client

import time


class IRCClient(Client):
    def onMessage(self, socket, message):
        
		# *** process incoming messages here ***
        print(message)
        return True

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = IRCClient()

# Start server
print('\nWelcome to Chat Systems')
client.start(ip, port)
time.sleep(1)

# While user is not quiting the server or keyboard interrupt keep recieving inputs from user and send to server 
while (True):
    try:
        message = input('\nEnter: ')
        if message == "quit":
            client.send(message.encode())
            client.stop()
            time.sleep(1)
            print('Disconected From Server')
            break
        else:
            client.send(message.encode())
    except KeyboardInterrupt:
        print('\nTo exit server type "quit" ')
        break