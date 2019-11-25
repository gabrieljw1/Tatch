class Vector(object):
    @staticmethod
    def scalarDivide(vector, div):
        return Vector(vector.x/div, vector.y/div, vector.z/div, vector.w/div)

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