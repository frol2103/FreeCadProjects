import FreeCAD
import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *
import window
import common
from common import *
import windows
import cabinet

workplanThick=20
workplanDepth=600
workplanHeight=840

def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Walls",allParts())

def allParts():
    parts = []
    util.concat(parts,workplan())
    return util.flatten([
        util.common(houseBox(),parts),
        ])
    
def workplan():
    return util.concats([
            workplanRightPart(),
            workplanPlates(),
            island(),
            ])

def workplanPlates():
    face = faceFromVectors([O,y(1060),xy(1060,1060),xy(1060,1060-workplanDepth),x(workplanDepth)])
    position =  xy(
                        600,
                        length-wallThick-1060
                    ) 

    return [rich(face \
                .extrude(z(workplanThick))) \
                .transO(position + z(workplanHeight)),
            rich(util.trimAlong(face, face.Edges[3],20) \
                    .extrude(z(workplanHeight)))\
                    .transO(position)
                ]


def workplanRightPart():
    wpWidth=width-1060-600-wallThick
    position=xy(
                1060+600, 
                length-wallThick-workplanDepth)

    c=cabinet.Cabinet(square(x(wpWidth),z(workplanHeight)).transO(position))
    return util.concats([
                box(wpWidth,workplanDepth,workplanThick)\
                                .transO(position + z(workplanHeight)),
                c.parts(),
                map(lambda f : f.extrude(y(10)),
                    map(lambda f: util.trimFace(f,3),
                    util.splitFaceAlong(c.face,x(1),[600,1100,1600,2200])))
            ])


def island():

    distBack=1680
    topWidth=820 #?
    topLength=1800 #?
    topHeight=890
    backCabinetDepth=500 #?
    backCabinetLength=1600
    frontCabinetDepth=300 #?
    frontCabinetLength=1000
    topOverHead=topWidth-backCabinetDepth-frontCabinetDepth

    cBack = cabinet.Cabinet(square(x(backCabinetLength), z(topHeight)) \
                .transO(xy(width-backCabinetLength - wallThick,
                    length -wallThick - distBack - topOverHead))) \
                .withDepth(backCabinetDepth)\
                .invertDir()

    cFront = cabinet.Cabinet(square(x(frontCabinetLength), z(topHeight)) \
                .transO(xy(width-frontCabinetLength - wallThick,
                    length -wallThick - distBack - topOverHead - backCabinetDepth - frontCabinetDepth))) \
                .withDepth(frontCabinetDepth)\

    return util.concats([
            box(topLength, topWidth, workplanThick)\
                .transO(v(width-topLength - wallThick,
                    length - topWidth - wallThick - distBack,
                    topHeight)),
            cBack.parts(),
            cFront.parts(),
            ])
