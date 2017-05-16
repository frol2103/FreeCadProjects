import util
from util import *
import FreeCAD
from FreeCAD import Base
import math

class Cabinet:
    face=None

    depth=600
    faceDepth=20
    dirFactor = 1

    def __str__(self):
        return "Cabinet "

    def __init__(self, face):
        self.face=face
    


    def parts(self):
        return [self.contentBox()]
                

    def normalO(self,size=1): 
        return mult(util.normalO(self.face,size), self.dirFactor)

    def perpendicularTo(self,edge):
        return util.perpendicularTo(edge,face)

    def box(self):
         return rich(self.face.extrude(self.normalO(self.depth)))

    def contentBox(self):
         return self.box() \
                 .cut(self.face.extrude(self.normalO(self.faceDepth)))


    def withDepth(self,d):
        self.depth = d
        return self

    def invertDir(self):
        self.dirFactor = -1
        return self
