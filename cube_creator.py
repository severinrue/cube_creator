
from pyfbsdk import *

import sys 

from PySide import *

import random

#cdBool checks if previous cubes should be deleted on executing the cubeCreator
#cbsBool checks if color by size has been chosen from the dropdown color options menu        
cdBool = False
cbsBool = False
#default values for the cubeCreator function to work with, in case the user doesn't enter any values
gotName = 'defaultName'
gotInterval = 50
gotScale = 5
scaleFactor = random.random() * (int(gotScale)) + (int(gotScale))
#global color used
globalColor = FBColor(0.8, 0.8, 0.8)
globalMaterial = FBMaterial('globalMat')
#the color options aside from the color picker
redMaterial = FBMaterial('redMat')
redMaterial.Diffuse = FBColor(1, 0, 0)
greenMaterial = FBMaterial('greenMat')
greenMaterial.Diffuse = FBColor(0, 1, 0)
blueMaterial = FBMaterial('blueMat')
blueMaterial.Diffuse = FBColor(0, 0, 1)
greyMaterial = FBMaterial('greyMat')
greyMaterial.Diffuse = FBColor(0.8, 0.8, 0.8)

   
def deletePrevious():    
    #making a new list instead of using cubeList, cause that one gets overwritten with every new call of the cubeCreator. could try appending
    foundComponents = FBComponentList()
    FBFindObjectsByName('*CCcube*', foundComponents, True, True)
    for comp in foundComponents:
        comp.FBDelete()                     
  
    
def createCube(positionVector, scaleFactor, rotationFactor1, rotationFactor2, rotationFactor3, name = 'defaultCubeName'):
    
    name = '%s_%d_%d_%d_CCcube' % ((str(gotName)), positionVector[0], positionVector[1], positionVector[2]) #str(gotText) cause otherwise it smh didn't get that gotText was a string already??
    cube = FBModelCube(name)
    cube.Show = True
    cube.Translation = positionVector
    cube.Scaling = FBVector3d(scaleFactor, scaleFactor, scaleFactor)
    cube.Rotation = FBVector3d(rotationFactor1, rotationFactor2, rotationFactor3)
       
    return cube
    
    
def cubeCreator():
    print "cubeCreator entered"   
    global globalMaterial
    globalMaterial.Diffuse = globalColor 
    cubeList = []    
    if cdBool == True:
        deletePrevious()    
    randomMaterial = FBMaterial('ranMat')
    randomMaterial.Diffuse = FBColor(random.random(), random.random(), random.random())                
    gap_interval = (int(gotInterval))
    for xPos in range (-100, 100, gap_interval):
        for yPos in range (0, 200, gap_interval):
            for zPos in range (-100, 100, gap_interval):
                 global scaleFactor                 
                 scaleFactor = random.random() * (int(gotScale)) + (int(gotScale))             
                 cube = createCube(FBVector3d(xPos, yPos, zPos), scaleFactor, random.uniform(0, 180), random.uniform(0, 180), random.uniform(0, 180))
                 if cbsBool == True:
                    if scaleFactor >= 8 and scaleFactor <= 9:                                           
                        cube.Materials.append(redMaterial)                        
                    elif scaleFactor >= 7 and scaleFactor < 8:
                        cube.Materials.append(greenMaterial)                    
                    elif scaleFactor < 7:
                        cube.Materials.append(blueMaterial)                                           
                    else:
                        cube.Materials.append(randomMaterial)                                   
                 else: 
                     cube.Materials.append(globalMaterial)
                 
                 cubeList.append(cube.LongName)
                                 
           
         
                                            
class cubeCreatorUI(QtGui.QWidget):
    
    def __init__(self):     
        super(cubeCreatorUI, self).__init__()  #super() creates a class that inherits all the methods and properties from another class
        
        self.initUI()
        
        print "init1 works"
##The self parameter is a reference to the current instance of the class, and is used to access variables that belong to the class.        
#It does not have to be named self , you can call it whatever you like, but it has to be the first parameter of any function in the class
        
        
    def initUI(self):
        
        self.setWindowTitle('CubeCreatorV4')
        self.setObjectName('cubeCreator_Widget')
        self.setLayout(QtGui.QHBoxLayout())
        self.setMinimumWidth(320)
        self.setMinimumHeight(400)
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)  
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)    
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 5))  #font for all tooltips
        
        self.setToolTip('This is my <b>CubeCreator</b> window :D')
    
        cb = QtGui.QCheckBox('DeletePrevious-Toggle', self)
        cb.resize(cb.sizeHint())
        cb.setToolTip('Enable to <b>delete previous</b> boxes on button click')
        cb.move(20, 80)
        cb.stateChanged.connect(self.deletionBoolCheck)
        print "deletion switch connected!" 

        btn = QtGui.QPushButton('CubeCreator', self)
        btn.setToolTip('Click to execute <b>cubeCreator</b> script')
        btn.resize(80, 40)#(btn.sizeHint()) #size hint is the preferred size of the widget
        btn.move(40, 30) #position of button
        btn.clicked.connect(cubeCreator)
        print "creator button connected!" 
        
        btn2 = QtGui.QPushButton('DeleteCubes', self)
        btn2.setToolTip('Click to <b>deleteCubes</b>')
        btn2.resize(80, 40)
        btn2.move(200, 30)
        btn2.clicked.connect(deletePrevious)
        print "delete button connected!" 
        
        self.lbl = QtGui.QLabel(self)
        self.lbl.move(20, 135)
        self.lbl.setText('Enter cube name:')
        qle = QtGui.QLineEdit(self)
        qle.move(25, 165)
        qle.setText(gotName)
        qle.textChanged[str].connect(self.onChanged1)
        
        self.lbl2 = QtGui.QLabel(self)
        self.lbl2.move(20, 210)
        self.lbl2.setText('Choose gap interval:\n%s' % str(gotInterval))
        qsl = QtGui.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        qsl.move(25, 240)
        qsl.setMinimum(20)
        qsl.setMaximum(80)
        qsl.setValue(50)
        qsl.setTickPosition(QtGui.QSlider.TickPosition.TicksBelow)
        qsl.setTickInterval(8)
        qsl.valueChanged[int].connect(self.onChanged2)
        
        self.lbl3 = QtGui.QLabel(self)
        self.lbl3.move(20, 275)
        self.lbl3.setText('Enter scale factor:') 
        self.qle3 = QtGui.QLineEdit(self)
        self.qle3.move(25, 305)
        self.qle3.setText(str(gotScale))
        self.qle3.textChanged[str].connect(self.onChanged3)
        self.qle3.editingFinished.connect(self.onFinished)
        
        '''self.lbl4 = QtGui.QLabel(self)
        self.lbl4.move(20, 260)
        self.lbl4.setText('Enter other thing:')
        qle4 = QtGui.QLineEdit(self)
        qle4.move(25, 290)
        qle4.textChanged[str].connect(self.onChanged4)'''
        
        self.lbl5 = QtGui.QLabel(self)
        self.lbl5.move(180, 135)
        self.lbl5.setText('Choose color:')
        
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("default - grey")
        comboBox.addItem("red")
        comboBox.addItem("green")
        comboBox.addItem("blue")
        comboBox.addItem("color by size")
        comboBox.addItem("color picker")
        comboBox.move(190, 165)
        comboBox.activated[str].connect(self.colorChosen)
        
        self.show()      
        
                            
    def onChanged1(self, text):         
        global gotName  
        if text == "":
            gotName = 'defaultName'
        else:      
            gotName = text        
        print gotName        
        
    def onChanged2(self, value):            
        global gotInterval        
        gotInterval = value 
        self.lbl2.setText('Choose gap interval:\n%s' % str(gotInterval))       
        print gotInterval        
        
    def onChanged3(self, text):          
        global gotScale 
        if text == "":
            gotScale = 5         
        else:
            gotScale = text    
        #self.lbl3.setText('Enter scale factor:\n%d' % int(gotScale))                    
        print gotScale      
        
    def onFinished(self):
        self.qle3.setText(str(gotScale))   
        
        
    def colorChosen(self, text):
        global cbsBool 
        cbsBool = False
        global globalColor
        if text == "default - grey":
            globalColor = FBColor(0.8, 0.8, 0.8)
        elif text == "red":
            globalColor = FBColor(1, 0, 0)
        elif text == "green":
            globalColor = FBColor(0, 1, 0)
        elif text == "blue":
            globalColor = FBColor(0, 0, 1)  
        elif text == "color picker":
            self.colorPicker()   
            print 'where is the picker?'  
        elif text == "color by size":
            cbsBool = True
            print 'size it up'
                 
                            
    def colorPicker(self):   
        print 'here is the picker!'
        global globalColor
        color = QtGui.QColorDialog.getColor()        
        pickerColor = FBColor()
        pickerColor[0] = color.red() / 255.00
        pickerColor[1] = color.green() / 255.00
        pickerColor[2] = color.blue() / 255.00
        globalColor = pickerColor
        print globalColor
        
        
    def deletionBoolCheck(self, state):
            
        global cdBool
    
        if state == QtCore.Qt.Checked:  
            cdBool = True
            print "Checked"
        
        else:
            cdBool = False
            print "Unchecked"
            
            
def main():    
    MenuInsert()
    print 'main works!' 
    
                
def MenuInsert():
    MenuMng = FBMenuManager()  
    MenuMng.InsertAfter(None, "THY", "Sev")
    SevMenu = MenuMng.GetMenu("Sev")
    SevMenu.InsertFirst("Cube Creator", 1)
    SevMenu.OnMenuActivate.Add(eventMenu)   
                                      
        
def eventMenu(control, event):    
    global cC
    cC = cubeCreatorUI()
    print 'hah!'       

     
if __name__ == '__main__' or __name__ == '__builtin__':
    main()
        

   