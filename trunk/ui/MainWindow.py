# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow,  QMessageBox
from PyQt4.QtCore import pyqtSignature

from Ui_MainWindow import Ui_MainWindow

from client import NetworkClient
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.tabWidget.setEnabled(False)
        self.client = NetworkClient()
        self.HouseCode = 'A'
        self.UnitCode = 1

#-------------------------------------------------------------------------------
    @pyqtSignature("")
    def on_pushButton_Connect_clicked(self):
        """
        Connect to Specified Server IP:PORT address
        """
        if( self.pushButton_Connect.text() == "Connect"):
            self.IP = self.lineEdit_ServerAddr.text()
            self.PORT = int( self.lineEdit_ServerPort.text() )
            if(self.client.Connect(self.IP,  self.PORT)):
                self.pushButton_Connect.setText("Disconnect")
                self.tabWidget.setEnabled(True)
            else:
                QMessageBox.critical(self, "Connection Error", "Could not connect to host", QMessageBox.Ok)
        else:
            self.client.Disconnect()
            self.pushButton_Connect.setText("Connect")
            self.tabWidget.setEnabled(False)
        
#-------------------------------------------------------------------------------    
    @pyqtSignature("")
    def on_pushButton_SendManualCmd_clicked(self):
        """
        Send a command to the server or local machine
        """
        cmd = str( self.lineEdit_CmdText.text() )
        
        if( self.checkBox_RemoteServer.isChecked() ):
            self.client.SendCmd( cmd )
            cmdResult = self.client.GetCmdResults()
            
        else:
            proc = os.popen(cmd)
            cmdResult = proc.read()
            
        self.textEdit_CmdOutput.append( cmdResult )
#-------------------------------------------------------------------------------    
    @pyqtSignature("")
    def on_pushButton_Exit_released(self):
        """
        Make sure to close the conenction to the server!
        """
        self.client.Disconnect()
#-------------------------------------------------------------------------------    
    @pyqtSignature("int")
    def on_dial_HouseCode_valueChanged(self, value):
        """
        Translate dial number [1-16] to a letter [A-P]
        """
        HouseCode = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        Selected = HouseCode[value-1]
        self.label_HouseCode.setText(str( Selected ))
        self.HouseCode = Selected
#-------------------------------------------------------------------------------    
    @pyqtSignature("")
    def on_pushButton_Off_released(self):
        """
        Sends the OFF command to the selected unit
        """
        # Build and send the bottle rocket command
        
        self.UnitCode = int(self.label_UnitCode.text())
        cmd = 'br --port=/dev/ttyS0 --house=' + self.HouseCode + ' --off='+ self.HouseCode + str(self.UnitCode)
                
        if( self.checkBox_RemoteServer.isChecked() ):
            self.client.SendCmd( cmd )
            cmdResult = self.client.GetCmdResults()
            
        else:
            proc = os.popen(cmd)
            cmdResult = proc.read()    

#-------------------------------------------------------------------------------    
    @pyqtSignature("")
    def on_pushButton_On_released(self):
        """
        Sends the ON command to the selected unit
        """      
        # Build and send the bottle rocket command
        
        self.UnitCode = int(self.label_UnitCode.text())
        cmd = 'br --port=/dev/ttyS0 --house=' + self.HouseCode + ' --on='+ self.HouseCode + str(self.UnitCode)
                
        if( self.checkBox_RemoteServer.isChecked() ):
            self.client.SendCmd( cmd )
            cmdResult = self.client.GetCmdResults()
            
        else:
            proc = os.popen(cmd)
            cmdResult = proc.read()    
