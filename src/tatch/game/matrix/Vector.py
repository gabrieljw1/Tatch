class Vector(object):
    @staticmethod
    def scalarDivide(vector, div):
        return Vector(vector.x/div, vector.y/div, vector.z/div, vector.w/div)

    @staticmethod
    def getVelocityFromPointToPoint(pointVector1, pointVector2, magnitude):
        dx = -pointVector1.x + pointVector2.x
        dy = -pointVector1.y + pointVector2.y
        dz = -pointVector1.z + pointVector2.z

        outputMagnitude = ( dx**2 + dy**2 + dz**2 )**0.5

        if (outputMagnitude == 0):
            return Vector(0,0,0)
        else:
            magnitudeRatio = magnitude / outputMagnitude
            return Vector(dx * magnitudeRatio, dy * magnitudeRatio, dz * magnitudeRatio)

    def __init__(self, x, y, z, w=1):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def __repr__(self):
        return f"Vector: [{self.x}, {self.y}, {self.z}, {self.w}]"

    def __eq__(self, other):
        return self.x == other.x and\
                self.y == other.y and\
                self.z == other.z and\
                self.w == other.w

    def __hash__(self):
        return hash( (self.x, self.y, self.z, self.w) )

    # Here, 'greater than' is defined as having a greater sum of x,y,z. This is
    #   used for vector hitbox calculation.
    def __gt__(self, other):
        return isinstance(other, Vector) and (self.x + self.y + self.z) > (other.x + other.y + other.z)