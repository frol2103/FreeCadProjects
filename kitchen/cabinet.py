import util
from util import *
import FreeCAD
from FreeCAD import Base
import math

class Cabinet:
    face=None

    depth=600
    faceDepth=40
    

    def __str__(self):
        return "Cabinet "

    def __init__(self, face):
        self.face=face
    


    def parts(self):
        return util.concat(
                [self.contentBox()],
                faceMargin(self.face)
                )

    def normalO(self,size=1): 
        return util.normalO(self.face,size)

    def perpendicularTo(self,edge):
        return util.perpendicularTo(edge,face)

    def box(self):
         return rich(self.face.extrude(self.normalO(self.depth)))

    def contentBox(self):
         return self.box() \
                 .cut(self.face.extrude(self.normalO(self.faceDepth)))


    def extrudeInCenter(self,face,depth):
        return rich(face.extrude(self.normalO(depth))) \
                .transO(self.normalO((self.boxDepth - depth)/2))

def faceMargin(face, margin=60):
    return util.cut(face,map(lambda e : util.faceAlong(face,e,margin),
            shapeFromRich(face).Edges))

