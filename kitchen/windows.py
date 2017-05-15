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

windowHeight=1000

def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Windows",allParts())

def allParts():
    return util.flatten(map(lambda x:x.parts(), allWindows()))

def allWindows():
    parts = []
    util.concat(parts,gardenWindows())
    util.concat(parts,windowDoor())
    util.concat(parts,hallDoor())
    util.concat(parts,workplanWindow())
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

    fixPartLength=900
    windowDoorLength=houseDiagonal-patioDiagonal-fixPartLength-(900)
    

    fixedFace=square(y(fixPartLength), z(wallMaxHeight)) \
                    .rotO(z(1),45) \
                    .transO(xy(width-3150, windowThick)) \
                    .transO(mult(xy(-1,1).normalize(),windowDoorLength))

    face=square(y(windowDoorLength), z(wallMaxHeight))
    doorWindow = internalWindow(face \
                    .rotO(z(1),45) \
                    .transO(xy(width-3150, windowThick)))
    fixedWindow = internalWindow(fixedFace)

    return [
            doorWindow[0].noFrameForEdges([0,1,2]),
            doorWindow[1].noFrameForEdges([0]),
            fixedWindow[0].noFrameForEdges([2]),
            fixedWindow[1],
            ]


def workplanWindow():
    windowLength=1200
    return [
            window.Window(square(x(windowLength),z(windowHeight))
                    .transO(v(width-windowLength-150,
                        length-wallThick,
                        wallMinHeight - 20 - windowHeight))
                ), \
            window.Window(square(y(windowLength),z(windowHeight))
                    .transO(v(width,
                        length-windowLength-150,
                        wallMinHeight - 20 - windowHeight))
                ) \
            ]

def windowsToCut():
    return util.concat(
            map(lambda x: x.box(),workplanWindow()),
            box(150,150,windowHeight) \
                .transO(v(width-150, 
                    length-150,
                    wallMinHeight - 50 - windowHeight))
            )

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
