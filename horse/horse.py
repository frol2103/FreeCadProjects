import sys
import os.path
#sys.path += [os.path.abspath("/home/frol/.FreeCAD/Mod/MyScripts")]
print(sys.path)
import partspattern
import side
import middlepart



def hreload():
    reload(partspattern)
    reload(side)
    reload(middlepart)

def showHorse():
    hreload();
    side.Side().showAll()
    middlepart.MiddlePart().showAll()


