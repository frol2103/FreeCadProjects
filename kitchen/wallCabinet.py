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


def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Wall Cabinet",allParts())

def allParts():
    cabinetWindowSpace=400
    cabinetWidth=length-islandTopWidth-islandDistBack - wallThick - windowThick - cabinetWindowSpace
    cabinetPosition=xy(width - wallThick - wallCabinetDepth, windowThick + cabinetWindowSpace)

    plantsHeigth=500
    plantsWidth=2000
    plantsPositionHeight=1200
    
    def plantBoxWithThickness(thickness):
        return util.box(thickness,\
            plantsWidth,\
            plantsHeigth)\
        .transO(cabinetPosition + z(plantsPositionHeight))

    plantBox=plantBoxWithThickness(wallCabinetDepth)
    plantBackBoard=plantBoxWithThickness(boardThick)\
                        .transO(x(wallCabinetDepth - boardThick))\
                        .withTexture(woodTexture)


    unlimittedFace = square(y(cabinetWidth),z(wallMaxHeight)) \
                        .transO(cabinetPosition)

    face = rich(unlimittedFace)\
            .cut(plantBox)\
            .commonFace(houseBox())\


    [bottomFace, middleFace, topFace] = util.splitFaceAlong(face,z(1),[plantsPositionHeight, plantsPositionHeight+plantsHeigth])

    
    return util.concats([
            util.splitFaceAlong(topFace, y(1),splitIn(cabinetWidth,3)),
            plantBackBoard,
           util.splitFaceAlong(bottomFace, y(1),splitIn(cabinetWidth,4)),
            rich(unlimittedFace.extrude(x(wallCabinetDepth)))\
                .cut(plantBox)\
                .common(houseBox())
            ])

         
