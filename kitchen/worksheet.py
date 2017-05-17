import util
from util import *
import Part
import kitchenCabinet

def test():
    util.clear()
    reload(util); 
    s = sBuild()
    bb = s.BoundBox
    box = util.box(max(1,bb.XLength),max(1,bb.YLength),max(1,bb.ZLength))\
            .transO(v(bb.XMin,bb.YMin, bb.ZMin))

    util.show(box)
    util.show(s)
    e = s.Edges[3]
    util.show(e)
    splits = util.splitFaceAlong(s,util.dir(e),[100,500,800]); 
    util.addGroup("splits",map(lambda f: util.trimFace(f,10),splits))

def sBuild(): 
    return square(x(2000), z(800))\
        .transO(v(400,236,548))\
        .rotO(y(12),56)

def island():
    util.clear()
    reload(kitchenCabinet)
    reload(util)
    util.addGroup("island", kitchenCabinet.island())

def upCabinet():
    util.clear()
    reload(kitchenCabinet)
    reload(util)
    util.addGroup("upcabinet", kitchenCabinet.upCabinet())
