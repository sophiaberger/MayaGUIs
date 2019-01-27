#######################################################
#important import try block at the top for Pyside#
from ctypes.wintypes import POINTL, DOUBLE
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

#######################################################
#GUI initializing block#

def getMayaWindow():
    prt = apiUI.MQtUtil.mainWindow()
    if prt is not None:
        return wrapInstance(long(prt), QMainWindow)

global myparent
myparent = getMayaWindow()

'''
Always rename based on the file to avoid confusion
'''
global motionToggleGUI
global hidden
global taskThreader
global dictionary

#######################################################
#for importing any new functions#
#######################################################


class myDialog(QDialog):
    def __init__(self, parent= None):
         #names need to match e.g. myDialog, floatDialog    
        super(myDialog, self).__init__()
        mainWidget = QWidget()

        self.setWindowTitle('Motion Trail Toggle')
    
        #cancel Button 
        cancelButton = QPushButton('OK')
        cancelButton.pressed.connect(self.close)
    
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(mainWidget)
        
         
        vLayout.addWidget(QLabel("You haven't selected anything!"))
        vLayout.addWidget(cancelButton)
    
        self.setLayout(vLayout)
        
    def warningLabel(self):
        self.show()
        
    def createMotionTrail(self, objectName):
        animStartTime = cmds.playbackOptions(query = True, animationStartTime = True)
        animEndTime = cmds.playbackOptions(query = True, animationEndTime = True)
        name = 'motionTrail' + objectName
        cmds.snapshot(objectName, motionTrail = True, increment = True, startTime = animStartTime, endTime = animEndTime, name = name, constructionHistory = True)
        
    
#######################################################  
#on click, functions         
def main():
    global motionToggleGUI
    try:
        motionToggleGUI.close()
        motionToggleGUI.deleteLater()
    except: pass
    initialObjects = cmds.ls(selection = True)
    motionToggleGUI = myDialog()
    if initialObjects:
        
        #check if any objects are selected
        for obj in initialObjects:
            try:
                cmds.delete('motionTrail'+obj+'*')
            except:
                motionToggleGUI.createMotionTrail(obj)    
        cmds.select(initialObjects)
    else:
        #throw warning message#
        motionToggleGUI.warningLabel()  
#initialize
#main class call    
if __name__ == '__main__':
    main()