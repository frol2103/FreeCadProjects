
import Part, FreeCAD, math
from FreeCAD import Base
import util
from truck.parts.truckParams import TruckParams
class Cabine:


    parts = None
    ###########################################################################
    ##########       Conf Methods                                    ##########
    ###########################################################################

    def __init__(self):
        self.parts = []
        self.makeCab()

    def makeCab():
        util.concat(self.parts,self.makeFloor())

    def getParts():
        return self.parts

    
    ###########################################################################
    ##########       Drawing Methods                                 ##########
    ###########################################################################
	
    def makeFloor(self,
            pnt=Base.Vector(0,side['thickness'],0),
            dir=Base.Vector(0, 0, 1)):
		floor_p = Part.makeBox(self.floor['length'],self.floor['width'],self.floor['thickness'],pnt,dir)
		h = Part.makeCylinder(self.steering['holeStickRadius'],self.floor['thickness'],Base.Vector(self.steering['xoffset'],self.steering['yoffset'],pnt.z),dir)
	 	return floor_p.cut(h)
	 
	def makeBack(self,pnt=Base.Vector(floor['length']-back['thickness'],side['thickness'],floor['thickness']),dir=Base.Vector(0, 0, 1)):
		back_p = Part.makeBox(self.back['thickness'],self.back['width'],self.back['height'],pnt,dir)
		return back_p 
	
	def makeFront(self,pnt=Base.Vector(0,side['thickness'],floor['thickness']),dir=Base.Vector(0, 0, 1)):
		front_p = Part.makeBox(self.front['thickness'],self.front['width'],self.front['height'],pnt,dir)
		
		wsv1 = pnt + Base.Vector(0,self.front['width']-self.front['windshield-smalledge'],self.front['windshield-botedge']);
		wsv2 = pnt + Base.Vector(0,self.front['width']-self.front['windshield-bigedge'],self.front['height']-self.front['windshield-topedge']);
		wsv3 = pnt + Base.Vector(0,self.front['windshield-bigedge'],self.front['height']-self.front['windshield-topedge']);
		wsv4 = pnt + Base.Vector(0,self.front['windshield-smalledge'],self.front['windshield-botedge']);
		
		wsl1 = Part.makeLine(wsv1,wsv2)
		wsl2 = Part.makeLine(wsv2,wsv3)
		wsl3 = Part.makeLine(wsv3,wsv4)
		wsl4 = Part.makeLine(wsv4,wsv1)
		
		wswire = Part.Wire([wsl1, wsl2, wsl3, wsl4]);
		
		windshield_p = Part.Face(wswire).extrude(Base.Vector(self.front['thickness'],0,0));
	 	return front_p.cut(windshield_p)
	
	def makeTop(self,pnt=Base.Vector(0,side['thickness'],side['height']-top['thickness']),dir=Base.Vector(0, 0, 1)):
		top_p = Part.makeBox(self.top['length'],self.top['width'],self.top['thickness'],pnt,dir)
		h = Part.makeCylinder(self.steering['holeStickRadius'],self.top['thickness'],Base.Vector(self.steering['xoffset'],self.steering['yoffset'],pnt.z),dir)
	  	return top_p.cut(h)
	
	def makePlate(self,pnt=Base.Vector(-plate['thickness'],0,-plate['height']+plate['voffset']),dir=Base.Vector(0, 0, 1)):
		p = Part.makeBox(self.plate['thickness'],self.plate['width'],self.plate['height'],pnt,dir)
		#p.makeFillet(self.plate['thickness']/2,p.Edges)
		
		return p
	
    def makeSeats(self,pnt=Base.Vector(floor['length']-back['thickness']-seat['depth'],0,floor['thickness']),dir=Base.Vector(0, 0, 1)):
		b1 = Part.makeBox(self.seat['depth'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['botThickness'],pnt,dir) 
		b2 = Part.makeBox(self.seat['depth'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['botThickness'],pnt + Base.Vector(0,self.floor['width']/2 + self.seat['betweenGap'],0),dir) 
		back1 = Part.makeBox(self.seat['backThickness'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['height'],pnt + Base.Vector(self.seat['depth']-self.seat['backThickness'],0,self.seat['botThickness']),dir) 
		back2 = Part.makeBox(self.seat['backThickness'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['height'],pnt + Base.Vector(self.seat['depth']-self.seat['backThickness'],self.floor['width']/2 + self.seat['betweenGap'],self.seat['botThickness']),dir) 
		return [b1, b2,back1,back2]
		
