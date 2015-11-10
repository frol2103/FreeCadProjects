import Part, FreeCAD, math
from FreeCAD import Base
from FreeCAD import Placement
import util

height = 550
shelfWidth = 600
depth = 400
section = 44
shelf1height = 300
mortThickness = 10

class WB:
    

    def showAll(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
        util.clear()
        parts = [];
        util.concat(parts,self.makeDrawerHolder())
        util.concat(parts,self.makeShelf1())
        doc=FreeCAD.activeDocument()
        grp=doc.addObject("App::DocumentObjectGroup", "Workbench")
        for p in parts:
            o =  doc.addObject("Part::Feature", "Part")
            o.Shape = p
            grp.addObject(o) 
        pass

            
    def makeDrawerHolder(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
        l1 = self.leg(pnt,dir,0)
        l2 = self.leg(pnt+Base.Vector(section/2+shelfWidth-2*mortThickness),dir,1)
        l3 = self.leg(pnt+Base.Vector(0,depth-section),dir,0)
        l4 = self.leg(pnt+Base.Vector(section/2+shelfWidth-2*mortThickness,depth-section),dir,1)
        return [l1,l2,l3,l4]

    def makeShelf1(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
        s1 = self.shelfSide(Base.Vector(section/2-mortThickness,mortThickness,shelf1height),dir,0)
        s2 = self.shelfSide(Base.Vector(shelfWidth+(section/2-mortThickness)-section/2,mortThickness,shelf1height),dir,1)
        f1 = self.shelfFace(Base.Vector(section/2-mortThickness,0,shelf1height),dir,0)
        f2 = self.shelfFace(Base.Vector(section/2-mortThickness,depth-section,shelf1height),dir,1)
        return [s1,s2,f1,f2]
    

    def leg(self, pnt, dir, side):
        l = Part.makeBox(section/2,section,height,pnt,dir)
        m1 = Part.makeBox(mortThickness,section,section,pnt+Base.Vector((1-side)*(section/2-mortThickness),0,shelf1height),dir)
        m2 = Part.makeBox(mortThickness,section,section,pnt+Base.Vector((1-side)*(section/2-mortThickness),0,height - section),dir)
        return l.cut(m1).cut(m2)
    
    
    def shelfSide(self, pnt, dir, side):
        p = Part.makeBox(section/2,depth-2*mortThickness,section,pnt,dir)
        return p

    def shelfFace(self, pnt, dir, side):
        p = Part.makeBox(shelfWidth,section,section,pnt,dir)
        m1 = Part.makeBox(section/2,section -mortThickness,section,pnt+Base.Vector(0,(1-side)*(mortThickness)),dir)
        m2 = Part.makeBox(section/2,section -mortThickness,section,pnt+Base.Vector(shelfWidth-section/2,(1-side)*(mortThickness)),dir)
        return p.cut(m1).cut(m2)
