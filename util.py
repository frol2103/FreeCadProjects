import FreeCAD
import Part
import sys
from FreeCAD import Base
from RichTopoShape import rich
from RichTopoShape import shapeFromRich
from RichTopoShape import RichTopoShape
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

def addGroup(name,parts):
    doc = FreeCAD.activeDocument()
    grp = doc.addObject("App::DocumentObjectGroup", name)

    for p in parts:
        rich(p).add(doc,grp)


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


def faceFromVectors(points):
    lines = []
    for i in range(0, len(points)):
        lines.append(Part.makeLine(points[i], points[(i + 1) % len(points)]))
    pass
    return rich(Part.Face(Part.Wire(lines)))

def partFromVectors(points, extrudeV=Base.Vector(0, 0, 0)):
    return rich(faceFromVectors(points).extrude(extrudeV))

def box(vx,vy,vz):
    return partFromVectors([O,x(vx), xy(vx,vy), y(vy)], z(vz))

def square(p1,p2):
    return faceFromVectors([O,p1,p1+p2,p2])

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
    if(len(l) == 0): return None
    return rich(reduce(lambda x,y : x.fuse(y), l))


def common(template, shapes):
    return map(lambda x: template.common(x), shapes)

def cut(template, shapes):
    return reduce(lambda t,x: t.cut(x), shapes, template)

def show(p):
    Part.show(shapeFromRich(p))

def flatten(l):
    return [item for sublist in l for item in sublist]

def normalO(face,size=1): 
    params=face.Surface.parameter(face.Edges[0].Vertexes[0].Point)
    normal=face.normalAt(params[0],params[1])
    return mult(normal,size)

def perpendicularTo(edge,face):
    v0 = edge.Vertexes[0].Point
    c=edge.copy()
    c.rotate(v0,
            normalO(face),
            90.0)

    p=(c.Vertexes[1].Point - c.Vertexes[0].Point).normalize()
    return p

def faceAlong(face,edge,dist):
    p=mult(perpendicularTo(edge, face),dist)
    v0=edge.Vertexes[0].Point
    v1=edge.Vertexes[1].Point
    pts = [v0+p,v1+p,v1-p,v0-p]
    trimFace = faceFromVectors(pts)
    return trimFace.common(face)

def trimAlong(face,edge,dist):
    return rich(face).cut(faceAlong(face,edge,dist)).Faces[0]

def trimFace(face, dist):
    return reduce(lambda f,e : trimAlong(f,e,dist), face.Edges,face)

def splitFaceAlong(face,direction ,splitDist):
    def no0(v): 
        if(v==0): return 1 
        else: return v

    bb=face.BoundBox
    dn = direction.normalize()
    d = v(abs(dn.x), abs(dn.y), abs(dn.z))

    print(d)

    xMax = abs(d.x) >= abs(d.y) and abs(d.x) >= abs(d.z)
    yMax = abs(d.y) >  abs(d.x) and abs(d.y) >= abs(d.z)
    zMax = abs(d.z) >  abs(d.x) and abs(d.z) >  abs(d.y)
    assert (xMax + yMax + zMax) == 1

    def principalDirectionLength():
        if(xMax): return bb.XLength / d.x
        elif(yMax): return bb.YLength / d.y
        elif(zMax): return bb.ZLength / d.z


    splitDistStart = concat(0,splitDist)
    splitDistEnd = concat(splitDist,principalDirectionLength())

    def part(i):
        start=splitDistStart[i]
        end=splitDistEnd[i]
        size=end-start

        sizeX=no0(size*d.x) if xMax else no0(bb.XLength)
        sizeY=no0(size*d.y) if yMax else no0(bb.YLength)
        sizeZ=no0(size*d.z) if zMax else no0(bb.ZLength)

        positionX=bb.XMin + start*d.x if xMax else bb.XMin
        positionY=bb.YMin +  start*d.y if yMax else bb.YMin
        positionZ=bb.XMin +  start*d.z if zMax else bb.ZMin
        

        return box(sizeX, sizeY,sizeZ)\
            .transO(v(positionX,positionY,positionZ))

    return map(lambda i : part(i).common(face).Faces[0],range(0,len(splitDistStart)))

def dir(edge):
    return (edge.Vertexes[1].Point - edge.Vertexes[0].Point).normalize()
