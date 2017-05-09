import math
from FreeCAD import Base
import util
from util import *
import Draft
from RichTopoShape import *


wallThick=300
interiorWallThick=100
wallMinHeight=2100
wallMaxHeight=3750

width=wt + 3700 + 600
length=6550 + wt +windowThick
