#import horse.horse; import line; import util
#reload(util); reload(line); reload(horse.horse); util.clear(); h = horse.horse.Horse(); h.makeSide();
import Part, FreeCAD, math
from FreeCAD import Base
import util
from line import Line
from middlepart import MiddlePart
class Side:
        
    thickness = 12;

    stopsWidth      = 50
    stopsHeight     = 60
    stopRatio       = 0.7
    botCurveWidth   = 630
    botCurveHeight  = 70

    vCurvesHeight   = 140
    vCurvesWidth    = 180
    vCurvesDepth    = 5
    maneOrigin      = Base.Vector(130,0,453)
    maneDestination = Base.Vector(145,0,425)


    horseWidth          = 270

    def showAll(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
        parts = [];
        util.concat(parts,self.makeSides())
        doc=FreeCAD.activeDocument() 
        grp=doc.addObject("App::DocumentObjectGroup", "Side") 

        for p in parts:
            o =  doc.addObject("Part::Feature", "Part")
            o.Shape = p
            grp.addObject(o) 
        pass 

    def makeSides(self):
        s1 = self.makeSide();
        s2 = self.makeSide();
        s2.translate(Base.Vector(0,self.horseWidth +self.thickness,0))
        sides = [s1, s2]
        sides_cut = []
        mps = MiddlePart().makeAll(True)
        for side in sides:
            for cutPart in mps:
                side = side.cut(cutPart)
            sides_cut.append(side)
        return sides_cut
        
    def makeSide(self):

        parts = []

        util.concat(parts,self.makeMane())
        util.concat(parts,self.makeHead())
        util.concat(parts,self.makeVCurveL())
        util.concat(parts,self.makePatin())
        util.concat(parts,self.makeVCurveR())
        util.concat(parts,self.makeBack())
        
        w = Part.Wire(parts)
        f = Part.Face(w)
        p = f.extrude(Base.Vector(0,self.thickness,0))
        return p

    def makePatin(self):
        stopsWidth      = self.stopsWidth    
        stopsHeight     = self.stopsHeight   
        botCurveWidth   = self.botCurveWidth 
        botCurveHeight  = self.botCurveHeight


        parts       = [];
        v11         = Base.Vector(stopsWidth,0,botCurveHeight);
        c11         = Base.Vector(stopsWidth + botCurveWidth/2,0,0);
        v12         = Base.Vector(stopsWidth+botCurveWidth,0,botCurveHeight);

        v21         = v11 + Base.Vector(-(1-self.stopRatio)*stopsWidth,0,stopsHeight)
        v22         = v11
        c21         = v11 + Base.Vector(-stopsWidth,0,stopsHeight/2)
    
        v31         = v12
        v32         = v31 + Base.Vector(0,0,stopsHeight)
        c31         = v31 + Base.Vector(stopsWidth,0,stopsHeight/2)
        

        parts.append(Part.Arc(v21,c21,v22).toShape())
        parts.append(Part.Arc(v11,c11,v12).toShape())
        parts.append(Part.Arc(v31,c31,v32).toShape())


        
        return parts 

    def makeVCurveL(self):
        vCurvesHeight   = self.vCurvesHeight
        vCurvesWidth    = self.vCurvesWidth 
        vCurvesDepth    = self.vCurvesDepth 
        
        v21         = Base.Vector(self.stopsWidth,0,self.botCurveHeight);
        v11         = v21 + Base.Vector(-(1-self.stopRatio)*self.stopsWidth,0,self.stopsHeight)

        v12         = v11+Base.Vector(vCurvesWidth,0,vCurvesHeight);
        l           = Line().fromPoints((v11.x, v11.z), (v12.x, v12.z))
        c11         = l.bissection().pointAtDist(-vCurvesDepth)
        cv11        = Base.Vector(c11[0],0,c11[1])
        a1 = Part.Arc(v12,cv11,v11)
        return a1.toShape()
        
    def makeVCurveR(self):
        parts = []
        vCurvesHeight   = self.vCurvesHeight
        vCurvesWidth    = self.vCurvesWidth 
        vCurvesDepth    = self.vCurvesDepth 
        v21         = Base.Vector(self.stopsWidth+self.botCurveWidth,0,self.botCurveHeight+self.stopsHeight);
        v22         = v21+Base.Vector(-vCurvesWidth,0,vCurvesHeight);
        l2          = Line().fromPoints((v21.x, v21.z), (v22.x, v22.z))
        p23         = l2.pointAtDist(l2.length() - self.stopsHeight)
        v23         = Base.Vector(p23[0], 0, p23[1])
        l3          = Line().fromPoints((v21.x, v21.z), (v23.x, v23.z))
        p21         = l3.bissection().pointAtDist(vCurvesDepth)
        c21         = Base.Vector(p21[0],0,p21[1])
        l4          = Line().fromPoints((v23.x, v23.z), (v22.x, v22.z))
        p31         = l4.bissection().pointAtDist(self.stopsWidth/2)
        c31         = Base.Vector(p31[0],0,p31[1])
        parts.append(Part.Arc(v21,c21,v23).toShape())
        parts.append(Part.Arc(v23,c31,v22).toShape())

        s1 = Part.Shape(parts)
        return parts
    
    def makeMane(self):
        a1 = Part.Line(self.maneOrigin, self.maneDestination)

        s1 = Part.Shape([a1])
        return s1

    def showLine(self,l,dist=None):
        v1 = Base.Vector(l.p0[0], 0 , l.p0[1])
        if dist==None:
            v2 = Base.Vector(l.p0[0] + l.direction[0], 0 , l.p0[1] + l.direction[1])
        else:
            p = l.pointAtDist(dist)
            v2 = Base.Vector(p[0],0,p[1])

        s1 = Part.Shape([Part.Line(v1,v2)])
        Part.show(s1)
    
    def makeBorder(self):
        l = 750
        h = 500
        p1 = Base.Vector(-10,0,-10)
        p2= p1 + Base.Vector(l,0,0)
        p3= p1 + Base.Vector(l,0,h)
        p4= p1 + Base.Vector(0,0,h)
        
        lines = util.linesFromPoints([p1,p2,p3,p4],True)
        Part.show(Part.Wire(lines))
        #Part.show(util.partFromVectors([p1,p2,p3,p4],Base.Vector(0,10,0)))


    def makeBack(self):
        points = []
        points.append(Base.Vector(500,0,270))
        points.append(Base.Vector(407,0,256))
        points.append(Base.Vector(323,0,291))
        points.append(Base.Vector(307,0,368))
        points.append(Base.Vector(177,0,473))
        points.append(Base.Vector(130,0,453))
        sp = Part.BSplineCurve()
        sp.interpolate(points,False)
        return Part.Wire(sp.toShape())

    def makeHead(self):
        points = []
        
        points.append(Base.Vector(145,0,425))
        points.append(Base.Vector(118,0,374))
        points.append(Base.Vector(129,0,299))
        points.append(Base.Vector(168,0,295))
        points.append(Base.Vector(203,0,320))
        points.append(Base.Vector(223,0,301))
        points.append(Base.Vector(215,0,270))

        sp = Part.BSplineCurve()
        sp.interpolate(points,False)
        return Part.Wire(sp.toShape())

    def makeRef(self):
        part = Part.makeBox(100,100,100,Base.Vector(550,0,300))
        Part.show(part)

        
        points = [] 
        c1  = Base.Vector(0,0,0)
        c2  = c1 + Base.Vector(750,0,0)
        c3  = c2 + Base.Vector(0,0, 500)
        c4  = c1 + Base.Vector(0,0, 500)
        lines = util.linesFromPoints([c1,c2,c3,c4],True)
        w = Part.Wire(lines)
        #f = Part.Face(w)
        p = w.extrude(Base.Vector(0,self.thickness))
        p.translate(Base.Vector(-10,0,-10))
        Part.show(p)
        
