import FreeCAD
import Part
from FreeCAD import Base

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
 
def concat(p1,p2):
    if(type(p1) != type([])):
        p1 = [p1]
    
    if(type(p2) == type([])):
        p1.extend(p2)
    else:
        p1.append(p2)


def partFromVectors(points,extrudeV=Base.Vector(0,0,0)):
    lines = []
    for i in range(0,len(points)):
        lines.append(Part.makeLine(points[i],points[(i+1)%len(points)]))
    pass
    return Part.Face(Part.Wire(lines)).extrude(extrudeV)

def linesFromPoints(points,closed = False):
    lines = []
    for i in range(0,len(points)-1):
        lines.append(Part.makeLine(points[i],points[(i+1)%len(points)]))
    if closed:
        lines.append(Part.makeLine(points[len(points)-1],points[0]))
    return lines

def mult(direction,size,origin = Base.Vector(0,0,0)):
    return origin + Base.Vector(size * direction.x,size * direction.y,size * direction.z)

def makeRef(p1,p2,p3, border):
        p4 = p1 + (p3-p2)    
        
        points = [] 
        lines = linesFromPoints([p1,p2,p3,p4],True)
        w = Part.Wire(lines)
        #f = Part.Face(w)
        p = w.extrude(border)
        Part.show(p)


