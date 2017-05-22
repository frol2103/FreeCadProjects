from util import *
import FreeCAD
from FreeCAD import Base
from PySide import QtGui
from pivy import coin

O=Base.Vector(0,0,0)

class RichTopoShape:
    color=(0.8,0.8,0.8)
    name="Part"
    transparency=0
    texturePath=None


    def __str__(self):
        return "RichTopoShape " + self.name + " " + str(self.color) + " of (" + str(self.delegate) + ")"

    def isRich(self):
        return True

    def __init__(self, shape):
        self.delegate = shape

    def __getattr__(self, attr):
        return getattr(self.delegate, attr)

    def rotO(self, v, angle):
        return self.rotate(O,v,angle)
    
    def rotate(self, v1, v2, angle):
        self.delegate.rotate(v1,v2,angle)
        return self

    def transO(self, v):
        self.translate(v)
        return self

    def cut(self, p):
        if(hasattr(p, 'delegate')):
          return RichTopoShape(self.delegate.cut(p.delegate))
        else:
          return RichTopoShape(self.delegate.cut(p))

    def cutFace(self,p):
        return rich(self.cut(p).delegate.Faces[0])
        

    def fuse(self, p):
        return RichTopoShape(self.delegate.fuse(shapeFromRich(p)))
    
    def common(self, p):
        return RichTopoShape(self.delegate.common(shapeFromRich(p)))
    
    def commonFace(self, p):
        return rich(self.common(p).delegate.Faces[0])

    def withTexture(self, texturePath):
        self.texturePath=texturePath
        return self

    def withColor(self,c):
        self.color=c
        return self
    
    def withName(self,n):
        self.name=n
        return self
    
    def withTransparency(self,t):
        self.transparency=t
        return self

    def add(self,doc,grp):
        if(self.delegate):
            o = doc.addObject("Part::Feature", self.name)
            o.Shape = self.delegate
            o.ViewObject.ShapeColor=self.color
            o.ViewObject.Transparency=self.transparency
            self.setTexture(o)
            grp.addObject(o)
    



    def setTexture(self,obj):
        if(self.texturePath):
            # get a jpg filename
            rootnode = obj.ViewObject.RootNode
            tex =  coin.SoTexture2()
            tex.filename = str(self.texturePath)
            rootnode.insertChild(tex,1) 

def shapeFromRich(p):
        if(hasattr(p, 'delegate')):
          return p.delegate
        else:
          return p

def rich(s):
    if(hasattr(s, 'isRich') and s.isRich()):
        return s
    else:
        return RichTopoShape(s)
        
