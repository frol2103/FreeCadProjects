#import horse.horse; import line; import util
#reload(util); reload(line); reload(horse.horse); util.clear(); h = horse.horse.Horse(); h.makeSide();
import Part, FreeCAD, math
from FreeCAD import Base
import util
from line import Line

class MiddlePart:
        
    thickness           = 12;
    sideThickness       = 15;
    keyThickness        = 15;

    tenonLength          = 3*keyThickness

    attachSize              = 50;
    attachWidth             = 3 * keyThickness
    attachCurveDepth        = 10
    attachHoleMarginStart   = 0;
    attachHoleMarginEnd     = 20;
    
    horseWidth          = 250
    
    feetHolderLength    = 111


    seatLength          = 220

    backCurveDepth      = 30
    backLength          = 175

    alpha               = 70
    r_alpha             = math.radians(alpha)
    alphaseat           = 10
    r_alphaseat              = math.radians(alphaseat)

    
    legHolderLength     = 110
    legSafeWidth        = 40
    legSafeHeight       = 90
    legSafeCurve1       = 20
    legSafeCurve2       = 20

    rodRadius           = 12.5
    rodOver             = 20
    rodTenonWidth       = 15

    def showAll(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
        parts = []; 
        util.concat(parts,self.makeAll())
        doc=FreeCAD.activeDocument() 
        grp=doc.addObject("App::DocumentObjectGroup", "middle") 
        for p in parts:
            o =  doc .addObject("Part::Feature", "Part")
            o.Shape = p
            grp.addObject(o) 
        pass 

    def makeAll(self, toCut=False):
        parts = []
        fh = self.feetHolder()
        lh = self.legHolder(toCut)
        s = self.seat(toCut)
        b = self.back(toCut)
        r = self.rod()

        fh.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), -(90+self.alpha))
        tx = (-math.cos(math.radians(90 - self.alpha)) + math.cos(self.r_alpha))*self.thickness
        tz = (math.sin(math.radians(90 - self.alpha)) + math.sin(self.r_alpha))*self.thickness
        fh.translate(Base.Vector(tx,0,tz))
        lh.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), -(self.alpha))
        tx = math.cos(self.r_alpha)*self.legHolderLength  
        tz= math.sin(self.r_alpha)*(self.legHolderLength) -self.thickness 
        s.rotate(Base.Vector(0,0,self.thickness), Base.Vector(0,1,0), self.alphaseat)
        s.translate(Base.Vector(tx,0,tz))
        b.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), -(70))
        tz += -self.seatLength*math.sin(self.r_alphaseat)+(1-math.cos(self.r_alpha))*self.thickness 
        tx += self.seatLength*math.cos(self.r_alphaseat) +math.sin(self.r_alpha)*self.thickness
        b.translate(Base.Vector(tx,0,tz))
        
        util.concat(parts, fh)
        util.concat(parts, lh)
        util.concat(parts, s)
        util.concat(parts, b)
        
        tr = Base.Vector(215,0,45)
        for p in parts:
            p.translate(tr)
        r.translate(Base.Vector(200,0,400))
        util.concat(parts, r)

        return parts
    
    def makeAll2(self, toCut=False):
        parts = self.makeAll()
        tr = Base.Vector(-215,0,-45)
        for p in parts:
            p.translate(tr)
            p.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), -20)
            p.translate(Base.Vector(123,0,0))
            Part.show(p)
        return parts

    def feetHolder(self):
        points = []
        c1  = Base.Vector(0,0,0)
        c2  = c1 + Base.Vector(self.feetHolderLength,0,0)
        c3  = c2 + Base.Vector(0,self.horseWidth,0)
        c4  = c1 + Base.Vector(0,self.horseWidth,0)
        
        tenonMargin = (self.feetHolderLength - self.tenonLength)/2
        t11 = c1 + Base.Vector(tenonMargin,0,0)
        t12 = t11+ Base.Vector(self.tenonLength)        
        t21 = c4 + Base.Vector(tenonMargin,0,0)
        t22 = t21+ Base.Vector(self.tenonLength)        
        
        points.append(c1)
        points += self.tenonPoints(t11,t12,Base.Vector(0,-1,0))
        points.append(c2)
        points.append(c3)
        points += self.tenonPoints(t22,t21,Base.Vector(0,1,0))
        points.append(c4)

        p = util.partFromVectors(points,Base.Vector(0,0,self.thickness))
        p.translate(Base.Vector(0,self.sideThickness,0))
        return p
    
    def legHolder(self,toCut=False):
        points = []
        c1  = Base.Vector(0,0,0)
        c2  = c1 + Base.Vector(self.legHolderLength,0,0)
        c3  = c2 + Base.Vector(0,self.horseWidth,0)
        c4  = c1 + Base.Vector(0,self.horseWidth,0)
        
        attachMargin = (self.legHolderLength- self.attachWidth)/2
        t11 = c1 + Base.Vector(attachMargin,0,0)
        t12 = t11+ Base.Vector(self.attachWidth)        
        t21 = c4 + Base.Vector(attachMargin,0,0)
        t22 = t21+ Base.Vector(self.attachWidth)        



        #block between legs
        b0  = util.mult((c3 - c2),0.5,c2)
        b11 = b0 + Base.Vector(0,-self.legSafeWidth)
        b21 = b0 + Base.Vector(0,self.legSafeWidth)        
        
        b12 = b11 + Base.Vector(self.legSafeHeight/2,self.legSafeCurve1)
        b22 = b21 + Base.Vector(self.legSafeHeight/2,-self.legSafeCurve1)        

        b13 = b11 + Base.Vector(self.legSafeHeight)
        b23 = b21 + Base.Vector(self.legSafeHeight)
        
        bt  = b0 + Base.Vector(self.legSafeCurve2 + self.legSafeHeight) 

        spPoints = [b11,b12,b13,bt,b23,b22,b21]


        points.append(b21)
        points.append(c3)
        points.append(c4)
        points.append(c1)
        points.append(c2)
        points.append(b11)

        p = util.partFromVectors(points,Base.Vector(0,0,self.thickness))
        lines = util.linesFromPoints(points)
        
        sp = Part.BSplineCurve()
        sp.interpolate(spPoints,False)
        
        lines.append(sp.toShape())
        w = Part.Wire(lines)
        f = Part.Face(w)
        p = f.extrude(Base.Vector(0,0,self.thickness))

        
        
        a1 = self.attachPart(t11,t12,Base.Vector(0,-1,0),toCut=toCut)
        a2 = self.attachPart(t21,t22,Base.Vector(0,1,0),toCut=toCut)
        part = p.fuse(a1).fuse(a2)
        part.translate(Base.Vector(0,self.sideThickness,0))
        return part

    def seat(self,toCut=False):
        points = [] 
        c1  = Base.Vector(0,0,0)
        c2  = c1 + Base.Vector(self.seatLength,0,0)
        c3  = c2 + Base.Vector(0,self.horseWidth,0)
        c4  = c1 + Base.Vector(0,self.horseWidth,0)
        
        t12 = c1+ Base.Vector(self.tenonLength)        
        t42 = c4+ Base.Vector(self.tenonLength)        
        t22 = c2- Base.Vector(self.tenonLength)        
        t32 = c3- Base.Vector(self.tenonLength)        
        
        points += self.tenonPoints(c1,t12,Base.Vector(0,-1,0))
        points += self.tenonPoints(t22,c2,Base.Vector(0,-1,0))
        points += self.tenonPoints(c3,t32,Base.Vector(0,1,0))
        points += self.tenonPoints(t42,c4,Base.Vector(0,1,0))

        part = util.partFromVectors(points, Base.Vector(0,0,self.thickness))
        part.translate(Base.Vector(0,self.sideThickness,0))
        return part
        
    def back(self,toCut=False):
        points = [] 
        c1  = Base.Vector(0,0,0)
        c2  = c1 + Base.Vector(self.backLength,0,0)
        c3  = c2 + Base.Vector(0,self.horseWidth,0)
        c4  = c1 + Base.Vector(0,self.horseWidth,0)

        #arc in the top
        av1 = util.mult((c3 - c2),0.5,c2) + Base.Vector(self.backCurveDepth) 
        
        c3c = c3 + Base.Vector(0,self.sideThickness,0)
        c2c = c2 + Base.Vector(0,-self.sideThickness,0)

        
        points.append(c3c)
        points.append(c3 + Base.Vector(-self.tenonLength,self.sideThickness,0))
        points.append(c3 + Base.Vector(-self.tenonLength,0,0))
        points.append(c4)
        
        points.append(c1)
        points.append(c2 + Base.Vector(-self.tenonLength,0,0))
        points.append(c2 + Base.Vector(-self.tenonLength,-self.sideThickness,0))
        points.append(c2c)

        
        lines = util.linesFromPoints(points)
        lines.append(Part.Arc(c2c,av1,c3c).toShape())
        w = Part.Wire(lines)
        f = Part.Face(w)
        p = f.extrude(Base.Vector(0,0,self.thickness))
        
        offset = Base.Vector((self.backLength - self.tenonLength - self.attachWidth)/2)
        att1v1 = offset + c1
        att1v2 = offset + c1+Base.Vector(self.attachWidth)
        att2v1 = offset + c4
        att2v2 = offset + c4+Base.Vector(self.attachWidth)
        a1 = self.attachPart(att1v1,att1v2,Base.Vector(0,-1,0),toCut=toCut)
        a2 = self.attachPart(att2v1,att2v2,Base.Vector(0,1,0),toCut=toCut)
        part = p.fuse(a1)
        part = part.fuse(a2)
        part.translate(Base.Vector(0,self.sideThickness,0))
        return part 
    
    
    def rod(self):
        part = Part.makeCylinder(self.rodRadius, self.horseWidth 
                + self.rodOver*2 + self.sideThickness*2
                ,Base.Vector(0,-self.rodOver), Base.Vector(0,1,0))
        boxXLength = self.rodRadius - self.rodTenonWidth/2
        box = Part.makeBox(boxXLength,self.rodOver+self.sideThickness,self.rodRadius*2
                            ,Base.Vector(-self.rodRadius,-self.rodOver, -self.rodRadius))

        part = part.cut(box)
        box.translate(Base.Vector(self.rodTenonWidth+boxXLength))
        part = part.cut(box)
        box.translate(Base.Vector(0,self.horseWidth+self.rodOver+self.sideThickness))
        part = part.cut(box)
        box.translate(Base.Vector(-self.rodTenonWidth-boxXLength))
        part = part.cut(box)
        return part

    def tenonPoints(self,p1,p2,direction,depth=sideThickness):
        translationVector =  util.mult(direction,depth)

        p11 = p1 + translationVector
        p21 = p2 + translationVector
        return [p1,p11,p21,p2]
    
    
    def attachPart(self,p1,p2,direction,size=attachSize,holeWidth=thickness, toCut=False):
        p12 = util.mult(direction,size-self.attachCurveDepth,p1)
        p22 = util.mult(direction,size-self.attachCurveDepth,p2)
        c   = util.mult((p2 - p1),0.5,p1) + util.mult(direction,size)
        a   = Part.Arc(p12,c,p22)
        lines = util.linesFromPoints([p22,p2, p1,p12])
        lines += [a.toShape()]
        w = Part.Wire(lines)
        p = Part.Face(w).extrude(Base.Vector(0,0,self.thickness))

        distHoleStart   = util.mult(direction,self.attachHoleMarginStart)
        distHoleEnd     = util.mult(direction,size-self.attachHoleMarginEnd)
        pi1 = util.mult((p2 - p1),1.0/3,p1) + distHoleStart
        pi2 = util.mult((p2 - p1),2.0/3,p1) + distHoleStart
        pi3 = util.mult((p2 - p1),1.0/3,p1) + distHoleEnd
        pi4 = util.mult((p2 - p1),2.0/3,p1) + distHoleEnd
        hole = util.partFromVectors([pi1,pi3,pi4,pi2], Base.Vector(0,0,self.thickness))
        if not toCut:
            attach = p.cut(hole)
        else:
            attach = p
        return  attach

    

