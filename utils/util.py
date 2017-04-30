import FreeCAD
import Part
from FreeCAD import Base
from RichTopoShape import rich
O = Base.Vector(0, 0, 0)


def clear():
    for p in FreeCAD.ActiveDocument.findObjects():
        FreeCAD.ActiveDocument.removeObject(p.Label)
    pass


def show(parts):
    if(type(parts) == type([])):
        for p in parts:
            Part.show(p)
        pass
    else:
        Part.show(parts)


def concat(p1, p2):
    if(p2 == None):
        return
    if(type(p1) != type([])):
        p1 = [p1]

    if(type(p2) == type([])):
        p1.extend(p2)
    else:
        p1.append(p2)
    return p1


def partFromVectors(points, extrudeV=Base.Vector(0, 0, 0)):
    lines = []
    for i in range(0, len(points)):
        lines.append(Part.makeLine(points[i], points[(i + 1) % len(points)]))
    pass
    return rich(Part.Face(Part.Wire(lines)).extrude(extrudeV))

def box(vx,vy,vz):
    return partFromVectors([O,x(vx), xy(vx,vy), y(vy)], z(vz))


def linesFromPoints(points, closed=False):
    lines = []
    for i in range(0, len(points) - 1):
        lines.append(Part.makeLine(points[i], points[(i + 1) % len(points)]))
    if closed:
        lines.append(Part.makeLine(points[len(points) - 1], points[0]))
    return lines


def mult(direction, size, origin=Base.Vector(0, 0, 0)):
    return origin + Base.Vector(size * direction.x, size * direction.y, size * direction.z)


def makeRef(p1, p2, p3, border):
        p4 = p1 + (p3 - p2)

        lines = linesFromPoints([p1, p2, p3, p4], True)
        w = Part.Wire(lines)
        p = w.extrude(border)
        Part.show(p)


def translate(parts, v):
    return map(lambda p: p.transO(v), parts)


def v(x, y, z):
    return Base.Vector(x, y, z)


def xy(x, y):
    return Base.Vector(x, y, 0)


def xz(x, z):
    return Base.Vector(x, 0, z)


def yz(y, z):
    return Base.Vector(0, y, z)


def x(v):
    return Base.Vector(v, 0, 0)


def y(v):
    return Base.Vector(0, v, 0)


def z(v):
    return Base.Vector(0, 0, v)

def fuse(l): 
    return rich(reduce(lambda x,y : x.fuse(y), l))
