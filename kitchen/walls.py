import FreeCAD
import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *

wallThick=30
interiorWallThick=10
wallMinHeight=210
wallMaxHeight=380

mh=wallMaxHeight
wt=wallThick
iwt=interiorWallThick

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
    util.concat(parts,houseBox())
    return parts
    
def mainWalls():
    return util.fuse([
            box(iwt,280+wt,mh).transO(xy(width-iwt-370-wt, length-280-wt)),
            box(60,iwt,mh).transO(y(length-wt-280)),
            box(285,windowThick,mh).transO(x(width-285-wt)),
            box(width-wt-60,wt,mh).transO(xy(60,length-wt)),
            box(wt,length,mh).transO(x(width-wt)),
            ])

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
        return partFromVectors(points,z(mh)).transO(x(border)).transO(toCenter).rotO(z(1),angle*i)

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


def houseBox():
    w = faceFromVectors([O,x(1000),xy(1000,1000),y(1000)])
    f = faceFromVectors([xy(500-1,500-1),xy(500+1,500-1),xy(500+1,501),xy(500-1,501)])
    f.translate(z(wallMaxHeight-wallMinHeight))

    b=util.box(1000,1000,wallMinHeight)
    roof=rich(Part.makeLoft([
        w.Wires[0],
        f.Wires[0],
    ],True)).transO(z(wallMinHeight))
    return (util.fuse([b,roof])
            .transO(xy(-1000+width,-1000+length)))



