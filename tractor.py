import Part, FreeCAD, math
from FreeCAD import Base
import util

class Cabine:
	floor 	= {'width':120, 'length':85, 'thickness':12}
	side  	= {'height':90, 'length':floor['length'], 'thickness':0}
	top   	= {'length':floor['length'], 'width':floor['width'], 'thickness':floor['thickness']}
	back  	= {'height':side['height']-floor['thickness']-top['thickness'], 'width':floor['width'], 'thickness':floor['thickness']}
	front 	= {'windshield-bigedge':20,'windshield-smalledge':10,'windshield-topedge':10,'windshield-botedge':30,  'height':side['height']-floor['thickness']-top['thickness'], 'width':floor['width'], 'thickness':floor['thickness']}
	plate 	= {'voffset':floor['thickness'] ,'height':2*floor['thickness'], 'width':floor['width'], 'thickness':floor['thickness']}
	axis 	= {'height':1.5*floor['thickness'], 'width':(floor['width'])/3, 'length':225}
	wheel	= {'radius':24, 'width':16}
	axle 	= {'side':2*(wheel['radius']*1.1 - axis['height']), 'width':floor['width']-2*wheel['width'], 'bhxoffset':50}
	steering= {'xoffset':floor['length']*2/3,'yoffset':floor['width']/2, 'stickRadius':4, 'holeStickRadius':4.5, 'axlePenetration':axle['side']/2.0, 'stickSurplus':4, 'guidonPenetration':8, 'guidonRadius':8}
	fwheel	= {'xoffset':axis['length']-60, 'innerHoleRadius':1.5, 'fwheelRadius':15,'thickness':5.3, 'insertionTrapezeBigBase':8}
	seat	= {'betweenGap':2*steering['stickRadius'], 'botThickness':floor['thickness'], 'backThickness':floor['thickness'], 'height':side['height']/2.5, 'depth':floor['length']/2.5}
	def showAll(self,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
		parts = [];
		util.concat(parts,self.makeFloor())
		util.concat(parts,self.makeBackAxle())
		util.concat(parts,self.makeFront())
		util.concat(parts,self.makeBack())
		util.concat(parts,self.makeTop())
		util.concat(parts,self.makePlate())
		#util.concat(parts,self.makeAxis())
		util.concat(parts,self.makeSteeringAxle())
		util.concat(parts,self.makeBackAxle())
	 	util.concat(parts,self.makeSteeringStick())
	 	util.concat(parts,self.make5Wheel())
	 	util.concat(parts,self.makeSeats())
		doc=FreeCAD.activeDocument() 
		grp=doc.addObject("App::DocumentObjectGroup", "Tractor") 
		for p in parts:
			o =  doc.addObject("Part::Feature", "Part")
			o.Shape = p
			grp.addObject(o) 
		pass 

	def makeFloor(self,pnt=Base.Vector(0,side['thickness'],0),dir=Base.Vector(0, 0, 1)):
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
	
 	def makeAxis(self,pnt=Base.Vector(0,(floor['width']-axis['width'])/2,-axis['height']),dir=Base.Vector(0, 0, 1)):
		p = Part.makeBox(self.axis['length'],self.axis['width'],self.axis['height'],pnt,dir)
		side = self.axis['height'] - self.plate['height']+self.plate['voffset']; 
		v1 = pnt + Base.Vector(side,0,0);
		v2 = pnt + Base.Vector(0,0,0);
	 	v3 = pnt + Base.Vector(0,0,side);
		vl1 = Part.makeLine(v1,v2)
		vl2 = Part.makeLine(v2,v3)
		vl3 = Part.makeLine(v3,v1)
		
		vwire = Part.Wire([vl1, vl2, vl3]);
		frontCut_p = Part.Face(vwire).extrude(Base.Vector(0,self.axis['width'],0));


		#hole for steering stick
		h = Part.makeCylinder(self.steering['holeStickRadius'],self.axis['width'],Base.Vector(self.steering['xoffset'],self.steering['yoffset'],pnt.z),dir)

		#hole for the pivot
		hp = Part.makeCylinder(self.fwheel['innerHoleRadius'],self.axis['height'],Base.Vector(self.fwheel['xoffset'],self.floor['width']/2,pnt.z),dir)

	 	return p.cut(frontCut_p).cut(h).cut(hp)
	
	def makeSteeringAxle(self,pnt=Base.Vector(steering['xoffset']-0.5*axle['side'],wheel['width'],-axis['height']-axle['side']),dir=Base.Vector(0, 0, 1)):
		p = Part.makeBox(self.axle['side'],self.axle['width'],self.axle['side'],pnt,dir)
		w1 = self.makeWheel(pnt + Base.Vector(self.axle['side']/2.0, -self.wheel['width'],self.axle['side']/2.0))
		w2 = self.makeWheel(pnt + Base.Vector(self.axle['side']/2.0, self.axle['width'],self.axle['side']/2.0))
		h = Part.makeCylinder(self.steering['stickRadius'],self.steering['axlePenetration'],Base.Vector(self.steering['xoffset'],self.steering['yoffset'],pnt.z+self.axle['side']-self.steering['axlePenetration']),dir)
		return [p.cut(h), w1, w2]
	
	def makeSteeringStick(self,pnt=Base.Vector(steering['xoffset'],steering['yoffset'],-steering['axlePenetration']-axis['height']),dir=Base.Vector(0, 0, 1)):
		stickHeight = self.steering['stickSurplus']+self.steering['guidonPenetration']+self.side['height']+self.floor['thickness']+self.top['thickness']
		s = Part.makeCylinder(self.steering['stickRadius'],stickHeight,pnt,dir)
		g = Part.makeSphere(self.steering['guidonRadius'],pnt + Base.Vector(0,0,stickHeight))
		
		return [s, g]
	
	def makeBackAxle(self,pnt=Base.Vector(axis['length']-axle['bhxoffset']-0.5*axle['side'],wheel['width'],-axis['height']-axle['side']),dir=Base.Vector(0, 0, 1)):
		p = Part.makeBox(self.axle['side'],self.axle['width'],self.axle['side'],pnt,dir) 
		w1 = self.makeWheel(pnt + Base.Vector(self.axle['side']/2.0, -self.wheel['width'],self.axle['side']/2.0))
		w2 = self.makeWheel(pnt + Base.Vector(self.axle['side']/2.0, self.axle['width'],self.axle['side']/2.0))
		return [p, w1, w2]
	
	def makeWheel(self,pnt,dir=Base.Vector(0, 1, 0)):
		p = Part. makeCylinder(self.wheel['radius'],self.wheel['width'],pnt,dir)
		return p

	def make5Wheel(self,pnt=Base.Vector(fwheel['xoffset'],floor['width']/2,0),dir=Base.Vector(0, 0, 1)):
		s = Part.makeCylinder(self.fwheel['fwheelRadius'],self.fwheel['thickness'],pnt,dir)
		h = Part.makeCylinder(self.fwheel['innerHoleRadius'],self.fwheel['thickness'],pnt,dir)
		
		tv1 = pnt + Base.Vector(0,self.fwheel['innerHoleRadius'],0);
		tv2 = pnt + Base.Vector(0,-self.fwheel['innerHoleRadius'],0);
		tv3 = pnt + Base.Vector(self.fwheel['fwheelRadius'],-self.fwheel['insertionTrapezeBigBase']/2,0);
		tv4 = pnt + Base.Vector(self.fwheel['fwheelRadius'],self.fwheel['insertionTrapezeBigBase']/2,0);
		tl1 = Part.makeLine(tv1,tv2)
		tl2 = Part.makeLine(tv2,tv3)
		tl3 = Part.makeLine(tv3,tv4)
		tl4 = Part.makeLine(tv4,tv1)
		
		twire = Part.Wire([tl1, tl2, tl3, tl4]);
		t = Part.Face(twire).extrude(Base.Vector(0,0,self.fwheel['thickness']));
		
		return s.cut(h).cut(t)

	def makeSeats(self,pnt=Base.Vector(floor['length']-back['thickness']-seat['depth'],0,floor['thickness']),dir=Base.Vector(0, 0, 1)):
		b1 = Part.makeBox(self.seat['depth'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['botThickness'],pnt,dir) 
		b2 = Part.makeBox(self.seat['depth'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['botThickness'],pnt + Base.Vector(0,self.floor['width']/2 + self.seat['betweenGap'],0),dir) 
		back1 = Part.makeBox(self.seat['backThickness'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['height'],pnt + Base.Vector(self.seat['depth']-self.seat['backThickness'],0,self.seat['botThickness']),dir) 
		back2 = Part.makeBox(self.seat['backThickness'],self.floor['width']/2 - self.seat['betweenGap'],self.seat['height'],pnt + Base.Vector(self.seat['depth']-self.seat['backThickness'],self.floor['width']/2 + self.seat['betweenGap'],self.seat['botThickness']),dir) 
		return [b1, b2,back1,back2]
		
	
	def makeSide(self, isRight=1,pnt=Base.Vector(0,0,0),dir=Base.Vector(0, 0, 1)):
		return Part()
         




	
