"""

Network server skeleton.

This shows how you can create a server that listens on a given network socket, dealing
with incoming messages as and when they arrive. To start the server simply call its
start() method passing the IP address on which to listen (most likely 127.0.0.1) and 
the TCP port number (greater than 1024). The Server class should be subclassed here, 
implementing some or all of the following five events. 

  onStart(self)
      This is called when the server starts - i.e. shortly after the start() method is
      executed. Any server-wide variables should be created here.
      
  onStop(self)
      This is called just before the server stops, allowing you to clean up any server-
      wide variables you may still have set.
      
  onConnect(self, socket)
      This is called when a client starts a new connection with the server, with that
      connection's socket being provided as a parameter. You may store connection-
      specific variables directly in this socket object. You can do this as follows:
          socket.myNewVariableName = myNewVariableValue      
      e.g. to remember the time a specific connection was made you can store it thus:
          socket.connectionTime = time.time()
      Such connection-specific variables are then available in the following two
      events.

  onMessage(self, socket, message)
      This is called when a client sends a new-line delimited message to the server.
      The message paramater DOES NOT include the new-line character.

  onDisconnect(self, socket)
      This is called when a client's connection is terminated. As with onConnect(),
      the connection's socket is provided as a parameter. This is called regardless of
      who closed the connection.

"""


import sys
from ex2utils import Server
import re

class EchoServer(Server):

    # The First Function called when the server is connected to the IP address and port 
    def onStart(self):
        """
        self.count -> to count the number of active users connected to the server.
        self.sk -> a dictionary to map the socket’s id to the socket objects of the client.
        self.names -> a dictionary to map the name of the user to the socket’s id.

        self.sk: socket.id -> socket._socket
        self.names: socket.name -> socket.id

        Two other variables socket.id and socket.name are initialised to each socket object to asscoiate with the id and their name 
        in the onConnect() function.
        """
        self.names = {} 
        self.count = 0
        self.sk = {}
        print("Server has started")
        print('\nClients connected to server: ',self.count)
    
        
    # When the client sends any message it is paased to this function to interpret the messages
    def onMessage(self, socket, message):
		# This function takes two arguments: 'socket' and 'message'.
		#     'socket' can be used to send a message string back over the wire.
		#     'message' holds the incoming message string (minus the line-return).


        (action,sep,msg) = message.strip().partition(' ')

        
        if(len(self.names) < self.count or socket.name == 'None'):
            
            # Check if the user is registered
            if(action != "reg"):
                warn = '\nYou must register name to send any messages'
                socket.send(warn.encode())

            # Check if any other user has the same name 
            elif(msg in list(self.names.keys())):
                m = '\n Name already registered'
                socket.send(m.encode())
            
            # Regsitering User Name
            elif(msg not in list(self.names.keys()) and re.search("[a-zA-Z_]+^[a-zA-Z0-9]+$",msg) == None):
                self.names[msg] = socket.id
                socket.name = msg
                m = '\n' + msg + ' Registered'
                socket.send(m.encode())
            
            # The name is invalid and must meet the requirements 
            else:
                warn = '\nNames must be alphanumeric of maximum 20 characters'
                socket.send(warn.encode())
        
        # List all active users
        elif(action == "active"):
            m = '\n Active Users: \n'
            for i in self.names.keys():
                m = m + i + '\n' 
            socket.send(m.encode())
        
        # Message to all users
        elif(action == "all"):
            n = list(self.names.keys())
            m = '\n'+n[socket.id-1] + ': ' + msg+ '\n\n'
            for i in self.sk.keys():
                s = self.sk[i]
                s.send(m.encode())
        
        # Message specific user
        elif('m-' in action):
            to = action.split('-')[1]
            
            # Check if the person messaging to exists 
            if(to in self.names.keys()):
                m = '\n'+ socket.name + ': ' + msg+ '\n\n'
                s = self.sk[self.names[to]]
                s.send(m.encode())
            
            # Person doesn't exists send error message to user
            else:
                socket.send(b'\n No such user registered')

        # Quit command     
        elif(action == "quit"):
            return False
        
        # Help command to list all commands
        elif(action == "help"):
            m = '\n\nCommand List\n1 - Quit Server using command ("quit")\n2 - Show all users using command("active)\n3 - Message all active users("all <msg>")\n4 - Message specific user ("m-<username> <msg>")\n\n5 - Register your Name using command ("reg <name>") Names must be alphanumeric of maximum 20 characters \n6 - Get command list ("help")'
            socket.send(m.encode())
        
        # If invalid command then print error to user
        else:
            m = '\n Wrong Command'
            socket.send(m.encode())
        
        return True

    # When server closes deallocate all the variables used and print message to the server 
    def onStop(self):
        self.count = 0
        if(len(self.sk) > 0):
            for i in list(self.sk.keys()):
                s = self.sk[i]
                s.send(b'halt')
        print('\nServer has stopped')
    
    # When new user connects then update the server variables with the user data, ie user's id  and the socket object of the user and the socket object of the user and the socket.id variable is initialised
    # socket.name is initalised in onConnect()
    def onConnect(self, socket):
        self.count = self.count + 1
        socket.id = self.count 
        socket.name = "None"
        self.sk[socket.id] = socket._socket
        
        print('\nClient Connected\nClients connected to server: ',self.count)
        m = '\n\nCommand List\n1 - Quit Server using command ("quit")\n2 - Show all users using command("active)\n3 - Message all active users("all <msg>")\n4 - Message specific user ("m-<username> <msg>")\n\n5 - Register your Name using command ("reg <name>") Names must be alphanumeric of maximum 20 characters \n6 - Get command list ("help")'
        socket.send(m.encode())
    
    # When new user connects then update the server variables by deleting the user data, ie user's id  and the socket object of the user and the socket.id and socket.name variables are deleted
    def onDisconnect(self, socket):
        self.count = self.count - 1
        del self.sk[socket.id]

        for key,value in self.names.items():
            if(value == socket.id):
                x = key
                del self.names[key]
                break
        del socket.id
        del socket.name
        
        
        print('\nClient '+ x +' Disconnected\nClients connected to server: ',self.count)
       



# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = EchoServer()

# Start server
server.start(ip, port)

