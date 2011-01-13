#!/usr/bin/env python
# client2.py

from socket import *
from time import time
from time import sleep
import sys

BUFSIZE = 4096

class NetworkClient:
       
    def __init__(self):
        self.sock = None
        self.bConnected = 0

    def Connect(self,  host,  port):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST,self.PORT)
        
        try:
            self.sock = socket( AF_INET, SOCK_STREAM)
            self.sock.connect( self.ADDR )
            self.bConnected = 1
        except:
            self.bConnected = 0
            
        return self.bConnected

    def SendCmd(self, cmd):
        if(self.bConnected):
            cmd = cmd.strip()
            self.sock.send(cmd)

    def GetCmdResults(self):
        if(self.bConnected):
            data = self.sock.recv( BUFSIZE )
            return data
        
    def Disconnect(self):
        if(self.bConnected):
            self.SendCmd('GOODBYE')
            self.bConnected = 0

if __name__ == '__main__':
    print "Testing client.py"

    client = NetworkClient()
    client.Connect('localhost', 29876 )
    
# Send some commands to the server
    client.SendCmd("ls")    
#   conn.sendCmd('br --port=/dev/ttyS0 --house=A --on=a1')
#   conn.sendCmd('br --port=/dev/ttyS0 --house=A --off=a1')
    print client.GetCmdResults()

    client.SendCmd('df -h')
    print client.GetCmdResults()

# Done, now close the connection
    client.Disconnect()
    
    print "Connection Closed"
