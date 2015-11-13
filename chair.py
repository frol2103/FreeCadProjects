import FreeCAD
import math
from FreeCAD import Base
import util
from util import *

angled = 25
angler = math.radians(angled)
angleComp = math.radians(90 - angled)
sina = math.sin(angler)
cosa = math.cos(angler)
tana = math.tan(angler)
height = 1500
legWidth = 100
thickness = 18
thickSmall = 18
chairWidth = (height - legWidth * tana) * math.cos(angleComp) + (legWidth / math.sin(angleComp))
chairDepth = 600
dirLeg = xz(sina, cosa)
grooveDepth = 5
internalPlankDepth = chairDepth - 2 * thickness + 2 * grooveDepth
plankDepth = chairDepth - 2 * thickness
firstLevel = 500
levelHeight = 50
hookWidthFromO=legWidth / math.sin(angleComp) + mult(dirLeg, thickSmall).x + 40


def showAll(pnt=Base.Vector(0, 0, 0), dir=Base.Vector(0, 0, 1)):
    util.clear()
    parts = [partFromVectors([O, x(1000), xy(1000, 1000), y(1000)], O - z(thickness))]

    util.concat(parts, util.translate(chair(), x(0)))
    # util.concat(parts,util.translate(chair('sym'), x(1500)))
    # util.concat(parts,util.translate(chair('tri'), x(3000)))

    doc = FreeCAD.activeDocument()
    grp = doc.addObject("App::DocumentObjectGroup", "Workbench")
    print(parts)
    for p in parts:
        o = doc.addObject("Part::Feature", "Part")
        if(hasattr(p, 'delegate')):
            o.Shape = p.delegate
        else:
            o.Shape = p
        grp.addObject(o)
    pass


def chair(legChoise='perp'):
    parts = []
    # concat(parts, leg(legChoise))
    # concat(parts, translate(leg(legChoise,True), y(chairDepth-thickness)))
    concat(parts, back())
    # concat(parts, seat())
    return parts


def leg(choise='perp', left=False):
    outsideGroove = y(0)
    insideGroove = y(thickness - grooveDepth)
    if(left):
        outsideGroove = insideGroove
        insideGroove = y(0)

    levels = map(lambda i: partFromVectors([O, x(1000), xz(1000, thickSmall), z(thickSmall)], y(grooveDepth)).transO(mult(dirLeg, firstLevel + levelHeight * i)).transO(insideGroove), range(0, 20))

    flatLeg = partFromVectors([O, xz(legWidth, legWidth * tana), xz(legWidth, height), z(height)], y(thickness)) \
        .cut(partFromVectors([O, z(10000), xz(thickSmall, 10000), x(thickSmall)], y(grooveDepth)).transO(x((legWidth - thickSmall) / 2)).transO(outsideGroove)) \
        .rotO(y(1), angled)

    for l in levels:
        flatLeg = flatLeg.cut(l)
    return concat([flatLeg], legSupport(choise))


def legSupport(choise):
    p1 = x(legWidth / math.sin(angleComp))
    p2 = p1 + z(legWidth) + x(legWidth / math.tan(angleComp))
    support = partFromVectors([p1, p2, xz(chairWidth, legWidth), x(chairWidth)], y(thickness))

    triangleBaseWidth = 1.5 * legWidth
    triangleHeight = (triangleBaseWidth / 2) * math.tan(angleComp)
    triangleL = p2
    triangleR = triangleL + x(triangleBaseWidth)
    triangleH = triangleL + x(triangleBaseWidth / 2) + z(triangleHeight)

    prop = {}
    prop['tri'] = partFromVectors([triangleL, triangleR, triangleH], y(thickness))

    angleCut = x(math.tan(math.radians(90 - 2 * angled)) * legWidth)
    prop['sym'] = partFromVectors([angleCut, z(legWidth), xz(450, legWidth), x(450)], y(thickness)).transO(O - angleCut).rotO(y(1), 90 - angled).transO(p1).transO(mult(dirLeg, 4 * legWidth)).cut(support)

    legWidthCutSize = (legWidth / math.sin(angleComp))
    prop['perp'] = partFromVectors([O, z(legWidth), xz(math.tan(angleComp) * (3 * legWidth - legWidthCutSize), legWidth), x(math.tan(angleComp) * (2 * legWidth - legWidthCutSize))], y(thickness))\
        .rotO(y(1), angled).transO(p1).transO(mult(dirLeg, 2 * legWidth))

    return [
        support,
        prop[choise]
    ]


def back():
    backHeight = 200
    supportXTrans = legWidth + thickSmall - mult(dirLeg, 3 * levelHeight).x
    return translate([
        box(thickSmall,plankDepth,backHeight)
            .transO(x(legWidth))
            .transO(y(thickness))
            .transO(z(50)),
                box(hookWidthFromO - supportXTrans, internalPlankDepth, thickSmall)
                    .transO(y(thickness - grooveDepth))
                    .transO(x(supportXTrans))
                    .fuse(hooks())
                    .transO(mult(dirLeg, 3 * levelHeight))
    ], mult(dirLeg, firstLevel + 12 * levelHeight))


def seat():
    seatWidth = 300
    return [
        partFromVectors([O, y(internalPlankDepth), xy(seatWidth, internalPlankDepth), x(seatWidth)], z(thickSmall))
            .transO(O - x(seatWidth / 2))
            .transO(y(thickness - grooveDepth))
            .transO(mult(dirLeg, 1100))
    ]


def hooks():
    def hookSide():
        return box(40, thickness - grooveDepth, thickSmall) \
            .fuse(box(legWidth + 20, thickness, thickSmall).transO(y(- thickness)).transO(x(- legWidth + 20))) \
            .transO(x(hookWidthFromO-40))
    
    return hookSide()
