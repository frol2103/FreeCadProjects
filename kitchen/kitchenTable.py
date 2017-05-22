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
    util.addGroup("Table",allParts())

def allParts():
    tableWidth=1200
    tableLength=3500
    tableThick=50
    

    return util.concats([
            box(tableWidth,tableLength,tableThick) \
                .transO(v(width-wallThick - wallCabinetDepth - 800 - tableWidth,
                    length-tableLength - wallThick -islandDistBack,
                    islandTopHeight
                    )) \
                .withTexture(woodTexture)

        ])


         
