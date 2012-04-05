import Part, FreeCAD, math
from FreeCAD import Base
import util
f

print(Truck)
class TrailerChassis:
    pivot = Truck.pivot;
    axle = Truck.trailerAxle;
    wheel=Truck.wheel;
    floor   = {'width':Truck.width, 'length':Truck.trailer['length'],'thickness':Truck.thickness}
    axle.update({'width':floor['width']-2*wheel['width']})
    pivot.update({'xoffset':math.sqrt(math.pow((Truck.axis['length'] - Truck.cabine['length']- Truck.fwheel['bxoffset']),2) - math.pow(Truck.width/2,2))-Truck.trailer['cabineMargin']})
    axis = Truck.axis.copy()
    axis.update({'pivotMargin':math.sqrt(math.pow((Truck.fwheel['bxoffset']),2) + math.pow(Truck.width/2,2))+Truck.trailer['axisMargin']})
    axis.update({'length':Truck.trailer['length']-pivot['xoffset']-axis['pivotMargin'],'xoffset':axis['pivotMargin']+pivot['xoffset']})
    trailerOrigin = Base.Vector(Truck.axis['length']-Truck.fwheel['bxoffset']-pivot['xoffset'],0,0)
    
    o_floor = None;
    o_axis  = None;

    def makeAxis(self,pnt=trailerOrigin + Base.Vector(axis['xoffset'],(floor['width']-axis['width'])/2,-axis['height']),dir=Base.Vector(0, 0, 1)):
        self.o_axis = Part.makeBox(self.axis['length'],self.axis['width'],self.axis['height'],pnt,dir)
        return self.o_axis

    def makeFloor(self,pnt=trailerOrigin,dir=Base.Vector(0, 0, 1)):
        p = Part.makeBox(self.floor['length'],self.floor['width'],self.floor['thickness'],pnt,dir)
        hs = Part.makeCylinder(self.pivot['radius'],self.pivot['inSize'],pnt+Base.Vector(self.pivot['xoffset'],self.floor['width']/2),dir)
        self.o_floor =  p.cut(hs)
        return self.o_floor;

    def makePivot(self,pnt=Base.Vector(Truck.axis['length']-Truck.fwheel['bxoffset'],floor['width']/2,-pivot['outSize']),dir=Base.Vector(0, 0, 1)):
        p = Part.makeCylinder(self.pivot['radius'],self.pivot['inSize']+self.pivot['outSize'],pnt,dir)
        return p
    

    def makeBackAxle(self,number=1,pnt=trailerOrigin + Base.Vector(floor['length']-axle['bxoffset']-0.5*axle['side'],wheel['width'],-axis['height']-axle['side']),dir=Base.Vector(0, 0, 1)):
        parts = []
        for i in range(number):
            print "\n axle"
            offset = Base.Vector(-(2*self.wheel['radius']+self.axle['betweenMargin'])*i,0,0);
            p = Part.makeBox(self.axle['side'],self.axle['width'],self.axle['side'],pnt+offset,dir) 
            w1 = self.makeWheel(offset + pnt + Base.Vector(self.axle['side']/2.0, -self.wheel['width'],self.axle['side']/2.0))
            w2 = self.makeWheel(offset + pnt + Base.Vector(self.axle['side']/2.0, self.axle['width'],self.axle['side']/2.0))
            parts.extend([p, w1, w2])
        else:
            return parts
    
    def makeWheel(self,pnt,dir=Base.Vector(0, 1, 0)):
        p = Part. makeCylinder(self.wheel['radius'],self.wheel['width'],pnt,dir)
        return p


    def makeTrailerChassis(self):
        parts = [];
        util.concat(parts,self.makeFloor())
        util.concat(parts,self.makeAxis())
        util.concat(parts,self.makePivot())
        util.concat(parts,self.makeBackAxle(2))
        return parts;
