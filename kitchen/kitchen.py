import FreeCAD
import math
from FreeCAD import Base
import Draft

import util
from util import *
import RichTopoShape

import walls

def hreload():
    util.clear()
    reload(util)
    reload(RichTopoShape)
    reload(walls)

def showAll():
    hreload();
    walls.showAll();


