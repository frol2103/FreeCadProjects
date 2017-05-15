import FreeCAD
import math
from FreeCAD import Base
import Draft

import util
from util import *
import RichTopoShape
import window
import walls
import common
import windows
import kitchenCabinet
import cabinet

def hreload():
    util.clear()
    reload(util)
    reload(RichTopoShape)
    reload(walls)
    reload(window)
    reload(common)
    reload(windows)
    reload(cabinet)
    reload(kitchenCabinet)

def showAll(showWindows=True):
    hreload();
    walls.showAll();
    if(showWindows): windows.showAll();
    kitchenCabinet.showAll()


