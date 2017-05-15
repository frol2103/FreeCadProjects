import util
from util import *
import FreeCAD
from FreeCAD import Base
import math

class Window:
    

    frameWidth=60
    frameThickness=30

    boxDepth=300

    glassThickness=10

    face = None
    edgesFrameIgnore=[]
    

    def __str__(self):
        return "Window " + str(self.face)

    def __init__(self, face):
        self.face = face
    
    def parts(self):
        return [
                self.glass(),
                self.frame(),
                ]

    def refPoint(self):
        return self.face.Edges[0].Vertexes[0].Point


    def normal(self):
        return Part.makeLine(self.refPoint(),self.normalAtRef())
    
    def normalO(self,size=1): 
        params=self.face.Surface.parameter(self.refPoint())
        normal=self.face.normalAt(params[0],params[1])
        return util.mult(normal,size)

    def show(self):
        map(lambda x: util.show(x), self.parts())

    def perpendicularTo(self,edge):
        v0 = edge.Vertexes[0].Point
        c=edge.copy()
        c.rotate(v0,
                self.normalO(),
                90.0)

        p=(c.Vertexes[1].Point - c.Vertexes[0].Point).normalize()
        return p

    def withBoxDepth(self,d):
        self.boxDepth = d
        return self

    def frame(self):
        edges = set([0,1,2,3]) - set(self.edgesFrameIgnore)
        if(len(edges) >0):
            return self.box().common(
                        util.fuse(map(lambda x: self.edgeFrame(self.face.Edges[x]),
                            edges))
                        ) \
                    .withColor((0.67,0.33,0.00)) \
                    .withName("windowFrame")


    def edgeFrame(self,edge):
        p=util.mult(self.perpendicularTo(edge),self.frameWidth)
        v0=edge.Vertexes[0].Point
        v1=edge.Vertexes[1].Point
        pts = [v0+p,v1+p,v1-p,v0-p]
        face = util.faceFromVectors(pts)
        return self.extrudeInCenter(face,self.frameThickness) \

    def box(self):
        return rich(self.face.extrude(self.normalO(self.boxDepth)))

    def glass(self):
        return self.extrudeInCenter(self.face,self.glassThickness) \
                .withColor((0.19,0.61,0.80)) \
                .withName("glass") \
                .withTransparency(90)

    def extrudeInCenter(self,face,depth):
        return rich(face.extrude(self.normalO(depth))) \
                .transO(self.normalO((self.boxDepth - depth)/2))

    def withFrameThickness(self,t):
        self.frameThickness = t
        return self

    def noFrameForEdges(self,e):
        self.edgesFrameIgnore=e
        return self
    
