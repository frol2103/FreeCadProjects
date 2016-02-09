import FreeCAD
import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *


backHeight=650
seatHeight=300
seatWidth=450
seatDepth=500
thickness=18

thicknessSide=25
r=seatHeight*3
angle=-10


#fava rocker

def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.clear()
    parts = []
    
    util.concat(parts,chair())
    doc = FreeCAD.activeDocument()
    grp = doc.addObject("App::DocumentObjectGroup", "Workbench")
    util.concat(parts,side(doc,grp))



    print(parts)
    for p in parts:
        o = doc.addObject("Part::Feature", "Part")
        if(hasattr(p, 'delegate')):
            o.Shape = p.delegate
        else:
            o.Shape = p
        grp.addObject(o)
    pass


def chair():
    return [box(thickness,seatHeight,seatWidth) \
        .fuse(box(thickness,seatHeight + backHeight, seatWidth).transO(x(seatDepth)))\
        .fuse(box(seatDepth,thickness, seatWidth).transO(y(seatHeight))) \
        .transO(x((-seatWidth/2))-y(r))  \
        .transO(z(-seatWidth))  \
        .rotO(z(1),angle)
        ]
        


def side(doc,grp):
    points = [
            xy(-530,-877),
            xy(-462,-321),
            xy(-85,-465),
            xy(85,-225),
            xy(299,-19),
            xy(433,-237),
            xy(415,-610),
            xy(380,-702),
            xy(183,-946)
            ]
    sp = Part.BSplineCurve()
    sp.interpolate(points,True)
    w = Part.Wire(sp.toShape())
    f = Part.Face(w)
    x = f.extrude(z(thicknessSide))
    c = Part.makeCylinder(r,thicknessSide,O,z(1))
    y = x.common(c)
    y.translate(z(-thicknessSide))
    return rich(y).rotO(z(1),20+angle)
