import FreeCAD
import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *

wallThick=300
interiorWallThick=100
wallMinHeight=2100
wallMaxHeight=3750

mh=wallMaxHeight
wt=wallThick
iwt=interiorWallThick

windowThick=150

width=wt + 3700 + 600
length=6550 + wt +windowThick

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
    return util.common(houseBox(),parts)
    
def mainWalls():
    return util.fuse([
            box(iwt,2800+wt,mh).transO(xy(width-iwt-3700-wt, length-2800-wt)),
            box(600,iwt,mh).transO(y(length-wt-2800)),
            box(2850,windowThick,mh).transO(x(width-2850-wt)),
            box(width-wt-600,wt,mh).transO(xy(600,length-wt)),
            box(wt,length,mh).transO(x(width-wt)),
            ])

def windowDoor():
    return [
            box(30,850+950,mh).rotO(z(1),45).transO(xy(width-2850-wt, windowThick))
            ]

def stairs():
    def side(i):
        angle=360/8.0
        wallThickness=100
        wt=wallThickness
        radius=900
        length=2*math.tan(math.radians(angle/2.0))*radius
        border=((2*radius)-length)/2
        toCenter=xy(-900,-900)
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
            ]).transO(xy(width-5000,length-5000))


def houseBox():
    w = faceFromVectors([O,x(10000),xy(10000,10000),y(10000)])
    f = faceFromVectors([xy(5000-1,5000-1),xy(5000+1,5000-1),xy(5000+1,5001),xy(5000-1,5001)])
    f.translate(z(wallMaxHeight-wallMinHeight))

    b=util.box(10000,10000,wallMinHeight)
    roof=rich(Part.makeLoft([
        w.Wires[0],
        f.Wires[0],
    ],True)).transO(z(wallMinHeight))
    return rich(util.fuse([b,roof])
            .transO(xy(-10000+width,-10000+length)))



