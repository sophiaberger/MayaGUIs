#######################################################

from __builtin__ import True
try:
    from PySide2 import  QtCore, QtWidgets
    from PySide2 import __version__ as Pyside__version__
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
    pysideVersion = Pyside__version__
  
except ImportError:
    from PySide import  QtCore
    from PySide import __version__ as Pyside__version__
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
    pysideVersion = Pyside__version__
 
from functools import wraps   

import sys, os
import math
from locale import str
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI   

def getMayaWindow():
    prt = apiUI.MQtUtil.mainWindow()
    if prt is not None:
        return wrapInstance(long(prt), QMainWindow)

global myparent
myparent = getMayaWindow()

global locatorGUI

class myDialog(QDialog):



    def addLocators(self, inputString):
        cmds.select(inputString +'*')
        trackerGroup = cmds.ls(selection = True)
        for i in trackerGroup:
            locator = cmds.spaceLocator()[0]
            cmds.parent(locator, i, relative = True)
            cmds.setAttr(locator + '.translateX', 0)
            cmds.setAttr(locator + '.translateY', 0)
            cmds.setAttr(locator + '.translateZ', 0)
        cmds.select(clear = True)
        locatorGUI.close()
        
    def __init__(self, parent= None):
         #names need to match e.g. myDialog, floatDialog 
         super(myDialog, self).__init__()
         mainWidget = QWidget()

         self.setWindowTitle('Fuse Asset Loader')

        #cancel Button 
         cancelButton = QPushButton('Cancel')
         cancelButton.pressed.connect(self.close)

        #okButton
         okButton = QPushButton("OK")
         okButton.clicked.connect(self.btnstate)
         
       

         #Scroll Area Layer add 
         
         self.inputString = QLineEdit()
         self.inputString.textChanged.emit(self.inputString.text())
        
         vLayout = QVBoxLayout(self)
         vLayout.addWidget(mainWidget)
        
         
         vLayout.addWidget(QLabel("Add Tracker Name Here: "))
         vLayout.addWidget(self.inputString)
         vLayout.addWidget(okButton)
         vLayout.addWidget(cancelButton)

         self.setLayout(vLayout)
         self.show()  

    def btnstate(self): 
        inputStr = self.inputString.text()
        self.addLocators(inputStr)   
        
        
        
def main():
    global locatorGUI
    try:
        locatorGUI.close()
        locatorGUI.deleteLater()
    except: pass
    #check if there are already locators in the scene called Tracker
    try:
        cmds.select('Tracker*')
        trackers = cmds.ls(selection = True)
        for i in trackers:
            locator = cmds.spaceLocator()[0]
            cmds.parent(locator, i, relative = True)
            cmds.setAttr(locator + '.translateX', 0)
            cmds.setAttr(locator + '.translateY', 0)
            cmds.setAttr(locator + '.translateZ', 0)
        cmds.select(clear = True)
    #otherwise, open the GUI
    except:
        locatorGUI = myDialog()
        locatorGUI.setWindowTitle('Locator Addition Window')
    
    
if __name__ == '__main__':
    main()