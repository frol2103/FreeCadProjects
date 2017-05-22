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

mh=wallMaxHeight
wt=wallThick
iwt=interiorWallThick



def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.addGroup("Walls",allParts())

def allParts():
    parts = []
    util.concat(parts,mainWalls())
    return util.concats([
        util.common(houseBox(),parts),
        stairs() \
                .common(houseBox()) \
                .withTexture('/home/francois/Downloads/wall-1733680_1920.jpg')
        ])
    
def mainWalls():
    windowsToCut = windows.windowsToCut()

    return reduce(lambda p,w : p.cut(w),windowsToCut,util.fuse([
            box(iwt,2800+wt,mh).transO(xy(width-iwt-3700-wt, length-2800-wt)),
            box(600,iwt,mh).transO(y(length-wt-2800)),
            box(width-wt-600,wt,mh).transO(xy(600,length-wt)),
            box(wt,length,mh).transO(x(width-wt)),
            ]))

def stairs():
    def side(i):
        angle=360/8.0
        wallThickness=100
        wt=wallThickness
        radius=900
        length=2*math.tan(math.radians(angle/2.0))*radius
        border=((2*radius)-length)/2
        toCenter=xy(-900,-900)
        bevel=wt/math.tan(math.radians(90-(angle/2.0)))
        points=[
                O,
                x(length),
                xy(length-bevel,wallThickness),
                xy(bevel,wallThickness),
                ]
        return partFromVectors(points,z(mh)).transO(x(border)).transO(toCenter).rotO(z(1),angle*i)

    return util.fuse([
            side(0),
            side(1),
            side(2),
            side(3),
            side(4),
            side(5),
            side(6),
            side(7),
            ]).transO(xy(width-5000,length-5000))

