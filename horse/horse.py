import sys
import os.path
#sys.path += [os.path.abspath("/home/frol/.FreeCAD/Mod/MyScripts")]
print(sys.path)
import partspattern
import side
import middlepart
import util
def hreload():
    util.clear()
    reload(partspattern)
    reload(side)
    reload(middlepart)

def showHorse():
    side.Side().showAll()
    middlepart.MiddlePart().showAll()


