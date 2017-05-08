from util import *
import FreeCAD
from FreeCAD import Base

O=Base.Vector(0,0,0)

class RichTopoShape:
    color=(0.8,0.8,0.8)

    def __str__(self):
        return "RichTopoShape of (" + str(self.delegate) + ")"

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

    def fuse(self, p):
        return RichTopoShape(self.delegate.fuse(shapeFromRich(p)))
    
    def common(self, p):
        print("Rich::common")
        return RichTopoShape(self.delegate.common(shapeFromRich(p)))

    def add(self,doc,grp):
        o = doc.addObject("Part::Feature", "Part")
        o.Shape = self.delegate
        o.ViewObject.ShapeColor=self.color
        grp.addObject(o)
        

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
        
