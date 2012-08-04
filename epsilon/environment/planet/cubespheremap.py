import math

from epsilon.geometry.euclid import Vector3

class CubeSphereMap(object):
    TOP =   0
    BACK =  1
    RIGHT = 2
    BOTTOM = 3
    FRONT = 4
    LEFT =  5
    
    face_names = ["TOP",
                  "BACK",
                  "RIGHT",
                  "BOTTOM",
                  "FRONT",
                  "LEFT"]
    
    # Convert the cube mapping to a vector on a unit sphere
    @staticmethod
    def get_sphere_vector(u, v, face):
        
        u = (u * 2.0) - 1.0
        v = (v * 2.0) - 1.0
        
        if face == CubeSphereMap.RIGHT:
            x = 1
            y = -v
            z = -u
        
        elif face == CubeSphereMap.LEFT:
            x = -1
            y = -v
            z = u
        
        elif face == CubeSphereMap.TOP:
            x = u
            y = 1
            z = v
            
        elif face == CubeSphereMap.BOTTOM:
            x = u
            y = -1
            z = -v
            
        elif face == CubeSphereMap.FRONT:
            x = u
            y = -v
            z = 1
            
        elif face == CubeSphereMap.BACK:
            x = -u
            y = -v
            z = -1
        
#        xo = x * math.sqrt(1.0 - y * y * 0.5 - z * z * 0.5 + y * y * z * z / 3.0)
#        yo = y# * math.sqrt(1.0 - z * z * 0.5 - x * x * 0.5 + z * z * x * x / 3.0)
#        zo = z * math.sqrt(1.0 - x * x * 0.5 - y * y * 0.5 + x * x * y * y / 3.0)
#        
#        return Vector3(xo, yo, zo)
        return Vector3(x, y, z).normalized()
    
    @staticmethod
    def get_face_from_position(x, y, z):
        face = None
        xa = math.fabs(x)
        ya = math.fabs(y)
        za = math.fabs(z)
        
        if xa > ya and xa > za:
            if x > 0:
                face = CubeSphereMap.RIGHT
            else:
                face = CubeSphereMap.LEFT
        elif ya > xa and ya > za:
            if y > 0:
                face = CubeSphereMap.TOP
            else:
                face = CubeSphereMap.BOTTOM
        else:
            if z > 0:
                face = CubeSphereMap.FRONT
            else:
                face = CubeSphereMap.BACK
        return face
    
    # Convert sphere mapping to cube coordinates
    @staticmethod
    def get_cube_coord(x, y, z):
        face = CubeSphereMap.get_face_from_position(x, y, z)
        xa = math.fabs(x)
        ya = math.fabs(y)
        za = math.fabs(z)
        
        xc = 0
        yc = 0
        
        if face == CubeSphereMap.RIGHT:
            if xa <= za:
                if x > 0:
                    xc = -1
                else:
                    xc = 1
            else:
                xc = -z / xa
            
            if xa <= ya:
                if y > 0:
                    yc = -1
                else:
                    yc = 1
            else:
                yc = -y / xa
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if x < 0.0 and xa > za and xa > ya:
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
        
        elif face == CubeSphereMap.LEFT:
            
            if xa <= za:
                if x > 0:
                    xc = 1.0
                else:
                    xc = -1.0
            else:
                xc = z / xa
            
            if xa <= ya:
                if y > 0:
                    yc = -1.0
                else:
                    yc = 1.0
            else:
                yc = -y / xa
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if x > 0.0 and xa > za and xa > ya:
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
                        
        elif face == CubeSphereMap.TOP:
            
            if ya <= xa:
                if x > 0:
                    xc = 1.0
                else:
                    xc = -1.0
            else:
                xc = x / ya
            
            if ya <= za:
                if z > 0:
                    yc = 1.0
                else:
                    yc = -1.0
            else:
                yc = z / ya
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if y < 0.0 and ya > xa and ya > za:
                
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
        
        elif face == CubeSphereMap.BOTTOM:
            
            if ya <= xa:
                if x > 0:
                    xc = 1.0
                else:
                    xc = -1.0
            else:
                xc = x / ya
            
            if ya <= za:
                if z > 0:
                    yc = 1.0
                else:
                    yc = -1.0
            else:
                yc = -z / ya
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if y < 0.0 and ya > xa and ya > za:
                
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
        
        elif face == CubeSphereMap.FRONT:
            
            if za <= xa:
                if x > 0:
                    xc = 1.0
                else:
                    xc = -1.0
            else:
                xc = x / za
            
            if ya <= za:
                if z > 0:
                    yc = -1.0
                else:
                    yc = 1.0
            else:
                yc = -z / ya
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if y > 0.0 and ya > xa and ya > za:
                
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
                        
        elif face == CubeSphereMap.BACK:
            
            if za <= xa:
                if x > 0:
                    xc = -1.0
                else:
                    xc = 1.0
            else:
                xc = -x / za
            
            if za <= ya:
                if y > 0:
                    yc = -1.0
                else:
                    yc = 1.0
            else:
                yc = -y / za
                
            # if the position is on the opposite face, we need to force the coordinates
            # to the edge of this face
            if z > 0.0 and za > xa and za > ya:
                
                if math.fabs(xc) > math.fabs(yc):
                    if xc > 0:
                        xc = 1.0
                    else:
                        xc = -1.0
                else:
                    if yc > 0:
                        yc = 1.0
                    else:
                        yc = -1.0
                        
        xc = max([0.0, min([1.0, (xc + 1.0) * 0.5] )])
        yc = max([0.0, min([1.0, (yc + 1.0) * 0.5] )])
        
        #return face, xc, yc
        return CubeSphereCoord(face, xc, yc)
        
        
    @staticmethod
    def get_sphere_position(u, v, face, radius):
        return CubeSphereMap.get_sphere_vector(u, v, face) * radius
    
class CubeSphereCoord(object):
    def __init__(self, face=CubeSphereMap.TOP, x=0, y=0):
        self._face = face
        self._x = x
        self._y = y
        
    def __repr__(self):
        return "Face: %s x: %f y: %f" % ( CubeSphereMap.face_names[self.face], self._x, self._y)
        
    @property
    def face(self):
        return self._face
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y