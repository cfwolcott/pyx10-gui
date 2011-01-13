#!/usr/bin/env python
# server2.py

from socket import *
import sys
import os

BUFSIZ = 4096
HOST = ''
PORT = 29876
ADDR = (HOST,PORT)

class ServCmd:
   def __init__(self):
       self.serv = socket( AF_INET,SOCK_STREAM)
#       self.serv.close()
       self.serv.bind((ADDR))
       self.cli = None
       self.listeningloop  = 0
       self.processingloop = 0
       self.run()

   def run(self):
       self.listeningloop = 1
       while self.listeningloop:
           self.listen()
           self.processingloop = 1
           while self.processingloop:
               self.procCmd()
           self.cli.close()
       self.serv.close()

   def listen(self):
       self.serv.listen(5)
       print 'Listening for Client'
       cli,addr = self.serv.accept()
       self.cli = cli
       print 'Connected to ', addr

   def procCmd(self):
       cmd = self.cli.recv(BUFSIZ)
       
       if not cmd:
        return
       
       print "Received command: ", cmd
       self.servCmd(cmd)
       if self.processingloop: 
           proc = os.popen(cmd)
           outp = proc.read()
           if outp:
               self.cli.send(outp)
           else   :
               self.cli.send('OK')
            
   def servCmd(self,cmd):
       cmd = cmd.strip()
       if cmd == 'GOODBYE': 
           self.processingloop = 0

if __name__ == '__main__':
   serv = ServCmd()
