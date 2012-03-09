from side import Side
from middlepart import MiddlePart
import util
import Part, FreeCAD, math
from FreeCAD import Base

mp = MiddlePart()

def makeMPs(reverse=False):
    fh = mp.feetHolder()
    lh = mp.legHolder()
    s = mp.seat()
    b = mp.back()
    parts = [fh,lh,s,b]
    fh.translate(Base.Vector(10))
    lh.translate(Base.Vector(120))
    s.translate(Base.Vector(300))
    b.translate(Base.Vector(600))
    for p in parts:
        if reverse:
            p.rotate(Base.Vector(0), Base.Vector(0,0,1),180)
        p.rotate(Base.Vector(0), Base.Vector(0,0,1),90)
        p.translate(Base.Vector(0,1100))
    return parts


util.makeRef(Base.Vector(0,0)
        ,Base.Vector(1220,0)
        ,Base.Vector(1220,2440)
        ,Base.Vector(0,0,18))

s1 = Side().makeSide()
s2 = Side().makeSide()
s3 = Side().makeSide()
s4 = Side().makeSide()
s5 = Side().makeSide()
s6 = Side().makeSide()

sides = [s1,s2,s3,s4,s5,s6]
for s in sides:
    s.rotate(Base.Vector(18), Base.Vector(1),-90)

s2.rotate(Base.Vector(0), Base.Vector(0,0,1),180)
s2.translate(Base.Vector(730,300+470))

s3.translate(Base.Vector(0,800))

s4.rotate(Base.Vector(0), Base.Vector(0,0,1),180)
s4.translate(Base.Vector(730,300+470+800))

s5.translate(Base.Vector(0,1600))

s6.rotate(Base.Vector(0), Base.Vector(0,0,1),180)
s6.translate(Base.Vector(730,300+470+1600))


for s in sides:
    s.translate(Base.Vector(10,10))
    Part.show(s)

for p in makeMPs():
    Part.show(p)
for p in makeMPs():
    Part.show(p)
for p in makeMPs(True):
    Part.show(p)
    

