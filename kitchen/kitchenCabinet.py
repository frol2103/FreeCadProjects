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
    return util.concat(
            workplanRightPart(),
            rich(faceFromVectors([O,y(1060),xy(1060,1060),xy(1060,1060-workplanDepth),x(workplanDepth)]) \
                .extrude(z(workplanThick)))
                .transO(v(
                        600,
                        length-wallThick-1060, 
                        workplanHeight
                    ))

            )

def workplanRightPart():
    wpWidth=width-1060-600-interiorWallThick
    position=xy(
                1060+600, 
                length-wallThick-workplanDepth)
    return util.concat(box(wpWidth,workplanDepth,workplanThick)\
            .transO(position + z(workplanHeight)),
            cabinet.Cabinet(square(x(wpWidth),z(workplanHeight)).transO(position)).parts()
            )

