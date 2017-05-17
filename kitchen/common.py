import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *


wallThick=300
interiorWallThick=100
wallMinHeight=2100
wallMaxHeight=3750
windowThick=150

width=wallThick + 3700 + 600

length=6550 + wallThick +windowThick
fridgeWallLength=2800

def houseBox():
    w = faceFromVectors([O,x(10000),xy(10000,10000),y(10000)])
    f = faceFromVectors([xy(5000-1,5000-1),xy(5000+1,5000-1),xy(5000+1,5001),xy(5000-1,5001)])
    f.translate(z(wallMaxHeight-wallMinHeight))

    b=util.box(10000,10000,wallMinHeight)
    roof=rich(Part.makeLoft([
        w.Wires[0],
        f.Wires[0],
    ],True)).transO(z(wallMinHeight))
    return rich(util.fuse([b,roof])
            .transO(xy(-10000+width,-10000+length)))


def heightAt(wallDist):
    angleRad=math.atan((wallMaxHeight-wallMinHeight)/5000.0)
    return math.tan(angleRad) * wallDist

def limitToHouseBox(parts):
    return map(lambda p: p.common(houseBox()),parts)

def limitFaceToHouseBox(part):
    return part.common(houseBox()).delegate.Faces[0]

def houseFloor():
        return square(x(100000),y(100000)).transO(xy(-10000+width,-10000+length))
