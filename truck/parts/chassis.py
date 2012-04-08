import Part, FreeCAD, math
from FreeCAD import Base
import util
from truck.parts.truckParams import TruckParams

class Chassis:

    axisLengt = 0;
    p_axis = None
    p_axles = None

    #util values
    axisBottom = TruckParams.wheel['radius']+TruckParams.axle['side']/2
    ###########################################################################
    ##########       Conf Methods                                    ##########
    ###########################################################################
    
    def __init__(self,axisLength = TruckParams.axis['length'], axleFront = 0, axleBack = 2):
        self.axisLength = axisLength
        self.p_axles = []
        self.p_axis = self.makeAxis()

        for i in range (axleFront):
            xOff = TruckParams.axle['fxoffset'] + i * (TruckParams.wheel['radius']*2 + TruckParams.axle['betweenMargin'])
            util.concat(self.p_axles,self.makeAxle(xOff))

        for i in range (axleBack):
            xOff = self.axisLength - TruckParams.axle['bxoffset'] - i * (TruckParams.wheel['radius']*2 + TruckParams.axle['betweenMargin'])
            util.concat(self.p_axles,self.makeAxle(xOff))

    def addSteering(self, xOffset = 40):
        util.concat(self.p_axles,self.makeAxle(xOffset,True))
                   

    def getParts(self):
        parts = []
        util.concat(parts, self.p_axis)
        util.concat(parts, self.p_axles)

        return parts;

    def showAll(self):
        for part in self.getParts(): 
            Part.show(part)
    


    ###########################################################################
    ##########       Drawing Methods                                 ##########
    ###########################################################################

    def makeAxis(self,
            pnt=Base.Vector(0,(TruckParams.width-TruckParams.axis['width'])/2,axisBottom),
            dir=Base.Vector(0, 0, 1)):
        p = Part.makeBox(self.axisLength,TruckParams.axis['width'],TruckParams.axis['height'],pnt,dir)
        return p

    def makeAxle(self,xOffset,directed=False):
        parts = []
        pnt=Base.Vector(xOffset, TruckParams.wheel['width'],TruckParams.wheel['radius']-TruckParams.axle['side']/2)
        p = Part.makeBox(TruckParams.axle['side'],TruckParams.axle['width'],TruckParams.axle['side'],pnt) 
        w1 = self.makeWheel(pnt + Base.Vector(TruckParams.axle['side']/2.0, -TruckParams.wheel['width'],TruckParams.axle['side']/2.0))
        w2 = self.makeWheel(pnt + Base.Vector(TruckParams.axle['side']/2.0, TruckParams.axle['width'],TruckParams.axle['side']/2.0))
        if directed:
            pntMidSteering = Base.Vector(pnt.x + TruckParams.axle['side']/2,pnt.y + TruckParams.axle['width']/2,pnt.z+TruckParams.axle['side']-TruckParams.steering['axlePenetration'])
            h = Part.makeCylinder(TruckParams.steering['stickRadius'],TruckParams.steering['axlePenetration']+TruckParams.axis['height'],
                    pntMidSteering)
            p = p.cut(h)
            Part.show(h)
            self.p_axis = self.p_axis.cut(h)
            util.concat(parts,self.makeSteeringStick(pntMidSteering))
        
        parts += [p,w1,w2]
        return parts
    
    def makeWheel(self,pnt,dir=Base.Vector(0, 1, 0)):
        p = Part. makeCylinder(TruckParams.wheel['radius'],TruckParams.wheel['width'],pnt,dir)
        return p

    def makeSteeringStick(self,pnt):
        stickHeight = TruckParams.steering['stickHeight']
        s = Part.makeCylinder(TruckParams.steering['stickRadius'],stickHeight,pnt)
        g = Part.makeSphere(TruckParams.steering['guidonRadius'],pnt + Base.Vector(0,0,stickHeight))
        
        return [s, g]
    
