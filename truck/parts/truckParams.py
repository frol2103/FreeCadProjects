import Part, FreeCAD, math
from FreeCAD import Base
import util
#import tractor
#import trailer

class TruckParams:
    width       = 90;
    thickness   = 9;
    cabine      = {'height':70,'length':60}
    axis        = {'length':170, 'height':18, 'width':30}
    wheel       = {'radius':18, 'width':12}
    steering    = {'stickRadius':4, 'holeStickRadius':4.5, 'stickHeight':200, 'guidonPenetration':8, 'guidonRadius':8,'axlePenetration':6}
    fwheel      = {'bxoffset':50, 'innerHoleRadius':2, 'fwheelRadius':15,'thickness':5.3, 'insertionTrapezeBigBase':8}
    axle        = {'fxoffset':40,'bxoffset':40,'betweenMargin':5 ,'width':66,'side':12}
    pivot       = {'outSize':10, 'inSize':5, 'radius':1.5}
    trailer     = {'cabineMargin':10, 'axisMargin':10, 'length':250}

