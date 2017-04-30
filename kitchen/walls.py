import FreeCAD
import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *

wallThick=30
wallMinHeight=210

mh=wallMinHeight
wt=wallThick

windowThick=15

width=wt + 370 + 60
length=655 + wt +windowThick

def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    parts = allParts()
    doc = FreeCAD.activeDocument()
    grp = doc.addObject("App::DocumentObjectGroup", "Workbench")



    for p in parts:
        o = doc.addObject("Part::Feature", "Part")
        if(hasattr(p, 'delegate')):
            o.Shape = p.delegate
        else:
            o.Shape = p
        grp.addObject(o)
    pass

def allParts():
    parts = []
    util.concat(parts,mainWalls())
    util.concat(parts,windowDoor())
    util.concat(parts,stairs())
    return parts
    
def mainWalls():
    return [
            box(wt,length,mh),
            box(285,windowThick,mh).transO(x(width-285-wt)),
            box(width,wt,mh).transO(y(length-wt)),
            box(wt,length,mh).transO(x(width-wt)),
            ]

def windowDoor():
    return [
            box(3,85+95,mh).rotO(z(1),45).transO(xy(width-285-wt, windowThick))
            ]

def stairs():
    def side(i):
        angle=360/8.0
        wallThickness=10
        wt=wallThickness
        radius=90
        length=2*math.tan(math.radians(angle/2.0))*radius
        border=((2*radius)-length)/2
        toCenter=xy(-90,-90)
        bevel=wt/math.tan(math.radians(90-(angle/2.0)))
        points=[
                O,
                x(length),
                xy(length-bevel,wallThickness),
                xy(bevel,wallThickness),
                ]
        return partFromVectors(points,z(10)).transO(x(border)).transO(toCenter).rotO(z(1),angle*i)

    return util.fuse([
            side(0),
            side(1),
            side(2),
            side(3),
            side(4),
            side(5),
            side(6),
            side(7),
            ]).transO(xy(width-500,length-500))
