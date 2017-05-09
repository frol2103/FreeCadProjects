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
    return map(lambda w:w \
                    .withFrameThickness(100) \
                    .withBoxDepth(100)
            ,
            [
            window.Window(square(y(windowDoorLength),z(wallMinHeight)) \
                    .rotO(z(1),45) \
                    .transO(xy(width-3150, windowThick)))
                    .noFrameForEdges([0,2]),
            window.Window(limitFaceToHouseBox(square(y(windowDoorLength),z(wallMaxHeight)) \
                    .rotO(z(1),45) \
                    .transO(v(width-3150, windowThick, wallMinHeight))))
            ])

