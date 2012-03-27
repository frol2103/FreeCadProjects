from side         import Side
from middlepart   import MiddlePart
import middlepart

import util
import Part, FreeCAD, math
from FreeCAD import Base

a3ht = Base.Vector(0,0,260)
a3lt = Base.Vector(360,0,0)

a3hf = Base.Vector(260,0,0)
a3lf = Base.Vector(0,360,0)
def makeSideCuts():
    p0 = Base.Vector(115,-4,10)
    lp = Base.Vector(100,0,0)
    util.makeRef(p0, p0+a3ht, p0+a3ht+a3lt+lp, Base.Vector(0,30))
    side = Side()
    Part.show(side.makeSides()[0])

def makeMP1():
    p0 = Base.Vector(-40,-20,0)
    util.makeRef(p0, p0+a3hf, p0+a3hf+a3lf, Base.Vector(0,0,30))
    mp = MiddlePart()
    Part.show(mp.feetHolder())
    Part.show(Part.makeBox(100,100,100, Base.Vector(110)))

def makeMP2():
    p0 = Base.Vector(-105,-18,0)
    util.makeRef(p0, p0+a3hf, p0+a3hf+a3lf, Base.Vector(0,0,30))
    mp = MiddlePart()
    p = mp.legHolder()
    p.rotate(Base.Vector(0), Base.Vector(0,0,1) ,20)
    Part.show(p)

def makeMP3():
    p0 = Base.Vector(-5,-25,0)
    util.makeRef(p0, p0+a3hf, p0+a3hf+a3lf, Base.Vector(0,0,30))
    mp = MiddlePart()
    p = mp.seat()
    b = mp.back(toCut=True)
    
    self=mp
    tx = math.cos(self.r_alpha)*(self.legHolderLength + (self.thickness / math.sin(self.r_alpha)))
    tz= math.sin(self.r_alpha)*(self.legHolderLength)
    p.translate(Base.Vector(tx,0,tz))
    
    b.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), -(70))
    tz2 = tz+self.thickness
    tx2 = tx+ self.seatLength - self.seatBackBorder
    b.translate(Base.Vector(tx2,0,tz2))
    p = p.cut(b)
    p.translate(Base.Vector(-tx,0,-tz))
    Part.show(p)

def makeMP4():
    p0 = Base.Vector(-70,-25,0)
    util.makeRef(p0, p0+a3hf, p0+a3hf+a3lf, Base.Vector(0,0,30))
    mp = MiddlePart()
    b = mp.back()
    
    Part.show(b)

def makeAttach():
    a4hf = Base.Vector(180,0,)
    a4lf = Base.Vector(0,250,0)
    p0 = Base.Vector(-20,-20,0)
    util.makeRef(p0, p0+a4hf, p0+a4hf+a4lf, Base.Vector(0,0,30))
    mp = MiddlePart()
    p = mp.attachPart(
            Base.Vector(0),
            Base.Vector(3*mp.thickness),
            Base.Vector(0,1))


    p2 = mp.attachPart(
            Base.Vector(0),
            Base.Vector(3*mp.thickness),
            Base.Vector(0,1))


    p3 = mp.attachPart(
            Base.Vector(0),
            Base.Vector(3*mp.thickness),
            Base.Vector(0,1))


    p4 = mp.attachPart(
            Base.Vector(0),
            Base.Vector(3*mp.thickness),
            Base.Vector(0,1))

    p2.translate(Base.Vector(80))
    p3.translate(Base.Vector(80,90))
    p4.translate(Base.Vector(0,90))
    Part.show(p)
    Part.show(p2)
    Part.show(p3)
    Part.show(p4)


