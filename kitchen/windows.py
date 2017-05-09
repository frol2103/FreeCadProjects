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


def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Windows",allParts())

def allParts():
    return util.flatten(map(lambda x:x.parts(), allWindows()))

def allWindows():
    parts = []
    util.concat(parts,gardenWindows())
    util.concat(parts,windowDoor())
    util.concat(parts,hallDoor())
    return parts


def gardenWindows():
    dest=x(width-2850-wallThick)
    return map(lambda x: window.Window(x)\
            .withFrameThickness(150) \
            .withBoxDepth(150),
    [
        util.square(x(2850),z(wallMinHeight)).transO(dest),
        util.faceFromVectors([O,x(2850),xz(2850,heightAt(wallThick)), z(heightAt(2850+wallThick))])
            .transO(dest+z(wallMinHeight)) \
    ])


def windowDoor():
    def diag(x): return math.sqrt(x*x*2)
    houseDiagonal=diag(5000)
    patioDiagonal=diag(3150)
    windowDoorLength=houseDiagonal-patioDiagonal-(900)
    
    face=square(y(windowDoorLength), z(wallMaxHeight))
    return internalWindow(face \
                    .rotO(z(1),45) \
                    .transO(xy(width-3150, windowThick)))



def internalWindow(face):
    lowTemplateBox=houseFloor().extrude(z(wallMinHeight))

    return map(lambda w:w \
                    .withFrameThickness(100) \
                    .withBoxDepth(100)
            ,
            [
                window.Window(face.commonFace(lowTemplateBox)) \
                        .noFrameForEdges([0,2]),
                window.Window(face.cutFace(lowTemplateBox).commonFace(houseBox())), \
            ])

def hallDoor():
    doorLength=5000-2800-wallThick-900
    print(doorLength)
    return internalWindow(
            square(y(doorLength), z(wallMaxHeight)).transO(y(length-2800-wallThick-doorLength))
            )
