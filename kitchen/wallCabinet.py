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
    cabinetWidth=length-islandTopWidth-islandDistBack - wallThick - windowThick
    depth=400

    return [
            rich(square(y(cabinetWidth),z(wallMaxHeight)) \
                .transO(xy(width - wallThick - depth, windowThick))\
                .extrude(x(depth))) \
                .common(houseBox())
            ]

         
