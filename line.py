import math;

class Line:
    p0          = None
    direction   = None

    def __init__(self, direction = [0,0], p0 = [0,0]):
        self.p0         = p0
        self.direction  = direction
    
    def fromPoints(self,p1,p2):
        return Line([(p2[0] - p1[0]), (p2[1] - p1[1])], p1)

    def bissection(self):
        tmp_dir = [1, None]
        tmp_dir[1] = - float(self.direction[0]*tmp_dir[0])/self.direction[1]
        tmp_p0 = [(self.direction[0]/2.0 + self.p0[0]), (self.direction[1]/2.0 + self.p0[1])]
        return Line(tmp_dir,tmp_p0)

    def point(self, p):
        print("p0:" +str(self.p0) + " dir:"+str(self.direction))
        if p[0] != None:
            p[1] = (float(p[0] - self.p0[0])/self.direction[0])* self.direction[1] + self.p0[1]
        else:
            p[0] = (float(p[1] - self.p0[1])/self.direction[1])* self.direction[0] + self.p0[0]
        return p

    def pointAtDist(self,dist,p=None):
        self.normalize()
        if p==None:
            p = self.p0
        return [p[0]+dist*self.direction[0],p[1]+dist*self.direction[1]]
   
    def normalize(self):
        length = self.length()
        self.direction[0] = float(self.direction[0]) / length
        self.direction[1] = float(self.direction[1]) / length
    
    def length(self):
        return math.sqrt(self.direction[0]**2 + self.direction[1]**2)

    
