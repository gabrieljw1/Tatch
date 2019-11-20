class Vector(object):
    @staticmethod
    def scalarDivide(vector, div):
        return Vector(vector.x/div, vector.y/div, vector.z/div, vector.w/div)

    def __init__(self, x, y, z, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f"Vector: [{self.x}, {self.y}, {self.z}, {self.w}]"