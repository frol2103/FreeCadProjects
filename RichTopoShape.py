from util import *
import FreeCAD
from FreeCAD import Base

O=Base.Vector(0,0,0)

class RichTopoShape:
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
        if(hasattr(p, 'delegate')):
          return RichTopoShape(self.delegate.fuse(p.delegate))
        else:
          return RichTopoShape(self.delegate.fuse(p))

def rich(s):
    if(hasattr(s, 'delegate')):
        return s
    else:
        return RichTopoShape(s)
        
