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

fridgeHeight=1780
fridgeWidth=910
fridgeDepth=700
fridgeAroundSpace=50

platesCabinetWidth=1060


def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Walls",allParts())

def allParts():
    parts = []
    util.concat(parts,workplan())
    return util.concats([
        util.common(houseBox(),parts),
        fridge(),
        fridgeCabinet(),
        upCabinet(),
        hoodCabinet(),
        ])
    
def workplan():
    return util.concats([
            workplanRightPart(),
            workplanPlates(),
            island(),
            ])

def workplanPlates():
    face = faceFromVectors([O,y(platesCabinetWidth),xy(platesCabinetWidth,platesCabinetWidth),xy(platesCabinetWidth,platesCabinetWidth-workplanDepth),x(workplanDepth)])
    position =  xy(
                        600,
                        length-wallThick-platesCabinetWidth
                    ) 

    return [rich(face \
                .extrude(z(workplanThick))) \
                .transO(position + z(workplanHeight)),
            rich(util.trimAlong(face, face.Edges[3],20) \
                    .extrude(z(workplanHeight)))\
                    .transO(position)
                ]


def workplanRightPart():
    wpWidth=width-platesCabinetWidth-600-wallThick
    position=xy(
                platesCabinetWidth+600, 
                length-wallThick-workplanDepth)

    c=cabinet.Cabinet(square(x(wpWidth),z(workplanHeight)).transO(position))
    return util.concats([
                box(wpWidth,workplanDepth,workplanThick)\
                                .transO(position + z(workplanHeight)),
                c.parts(),
                extrudeFace(
                    map(lambda f: util.trimFace(f,3),
                    util.splitFaceAlong(c.face,x(1),[600,1100,1600,2200])))
            ])


def extrudeFace(faces, dirFactor=1): 
    return map(lambda f : f.extrude(util.mult(y(10),dirFactor)), faces)

def island():

    distBack=1680
    topWidth=990
    topLength=2000
    topHeight=890
    backCabinetDepth=560
    backCabinetLength=1600
    frontCabinetDepth=300
    frontCabinetLength=1000
    topOverHead=topWidth-backCabinetDepth-frontCabinetDepth

    cBack = cabinet.Cabinet(square(x(backCabinetLength), z(topHeight)) \
                .transO(xy(width-backCabinetLength - wallThick,
                    length -wallThick - distBack - topOverHead))) \
                .withDepth(backCabinetDepth)\
                .invertDir()

    cBackFace = extrudeFace(util.flatten(map(lambda f:util.splitFaceAlong(f,z(1),[topHeight/2]),
            util.splitFaceAlong(cBack.face,x(1),[backCabinetLength/2]))),
            -1
            )

    cFront = cabinet.Cabinet(square(x(frontCabinetLength), z(topHeight)) \
                .transO(xy(width-frontCabinetLength - wallThick,
                    length -wallThick - distBack - topOverHead - backCabinetDepth - frontCabinetDepth))) \
                .withDepth(frontCabinetDepth)\
    
    cFrontFace = extrudeFace(util.splitFaceAlong(cFront.face,x(1),[frontCabinetLength/2]))

    return util.concats([
            box(topLength, topWidth, workplanThick)\
                .transO(v(width-topLength - wallThick,
                    length - topWidth - wallThick - distBack,
                    topHeight)),
            cBack.parts(),
            cFront.parts(),
            cBackFace,
            cFrontFace,
            ])


fridgeBoxPosition = xy(600,length-fridgeWallLength-wallThick)

def fridgeBox():
    return box(fridgeDepth, fridgeWidth + 2* fridgeAroundSpace,fridgeHeight+fridgeAroundSpace)\
            .transO(fridgeBoxPosition)
        
def fridge():
    return box(fridgeDepth, fridgeWidth,fridgeHeight)\
            .transO(fridgeBoxPosition + y(fridgeAroundSpace))


def fridgeCabinet():
    c = cabinet.Cabinet(square(y(fridgeWallLength - platesCabinetWidth ),z(wallMaxHeight)) \
            .transO(xy(600 + 600,length-fridgeWallLength-wallThick)) \
            .cutFace(fridgeBox()) \
            .commonFace(houseBox()))

    fridgeBoxLength=fridgeBox().BoundBox.YLength

    faces = util.splitFaceAlong(c.face, y(1), [fridgeBoxLength/2,fridgeBoxLength])
    fridgeBoxHeight = fridgeBox().BoundBox.ZLength
    return util.concats([
        c.parts(),
        extrudeFace(util.concats([
                faces[0],
                faces[1],
                util.splitFaceAlong(faces[2], z(1), util.concat(splitIn(fridgeHeight,5), fridgeHeight))
            ])),
        ])


def splitIn(length, howMany):
    return map(lambda i : i*(length/howMany),range(1,howMany))

hoodHeight=1700

def upCabinet():
    cabinetWidth=width-platesCabinetWidth-workplanWindowLength -600 - wallThick +150
    c=cabinet.Cabinet(square(x(cabinetWidth), z(2000))\
            .transO(v(platesCabinetWidth+600, length-wallThick-600, hoodHeight))\
            .commonFace(houseBox())
            )

    faces = util.splitFaceAlong(c.face, x(1), [cabinetWidth/2])

    return util.concats([
        util.common(houseBox(),c.parts()),
        faces,
        ])



def hoodCabinet():
    face = util.faceFromVectors([O,\
            y(platesCabinetWidth),\
            xy(platesCabinetWidth,platesCabinetWidth),\
            xy(platesCabinetWidth, platesCabinetWidth-600),\
            x(600),
            ])

    return rich(face \
            .transO(z(hoodHeight))\
            .transO(xy(600,length-wallThick-platesCabinetWidth))\
            .extrude(z(1000)))\
            .common(houseBox())
