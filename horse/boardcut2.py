from side import Side
from middlepart import MiddlePart
import util
import Part, FreeCAD, math
from FreeCAD import Base

mp = MiddlePart()


p1 = Base.Vector(100,0,0)
p2 = Base.Vector(100,1000,0)
p3 = Base.Vector(100,2000,0)
util.makeRef(
         p1+Base.Vector(0,0)
        ,p1+Base.Vector(1220,0)
        ,p1+Base.Vector(1220,900)
        ,Base.Vector(0,0,18))


util.makeRef(
         p2+Base.Vector(0,0)
        ,p2+Base.Vector(1220,0)
        ,p2+Base.Vector(1220,900)
        ,Base.Vector(0,0,18))


util.makeRef(
         p3+Base.Vector(0,0)
        ,p3+Base.Vector(1220,0)
        ,p3+Base.Vector(1220,640)
        ,Base.Vector(0,0,18))

def addMPParts():
    fh = mp.feetHolder()
    lh = mp.legHolder()
    s = mp.seat()
    lhr = mp.legHolder()
    lhr.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),180)
    b = mp.back()
    br = mp.back()
    br.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),180)
    fh.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    lh.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    s.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    lhr.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    b.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    br.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    ty = 0
    fh.translate(Base.Vector(0,ty,0))
    ty += 150
    lh.translate(Base.Vector(0,ty,0))
    ty += 250
    lhr.translate(Base.Vector(-280,ty+200,0))
    ty += 250
    s.translate(Base.Vector(0,ty,0))
    ty += 250
    b.translate(Base.Vector(0,ty,0))
    ty += 250
    br.translate(Base.Vector(-280,ty+200,0))
    Part.show(fh)
    Part.show(lh)
    Part.show(lhr)
    Part.show(s)
    Part.show(b)
    Part.show(br)




    

