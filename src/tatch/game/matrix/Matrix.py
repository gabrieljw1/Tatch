import numpy

from game.matrix.Vector import Vector

# A matrix object. Self explanatory.
class Matrix(object):
    @staticmethod
    def generateIdentity(rows, cols):
        output = Matrix(rows, cols)

        for row in range(rows):
            for col in range(cols):
                if (row == col):
                    output.values[row][col] = float(1.0)

        return output

    # Generate the inverse of a given matrix.
    @staticmethod
    def inverse(matrix):
        output = Matrix(matrix.rows, matrix.cols, None)

        output.values = numpy.linalg.inv( matrix.values ).tolist()

        return output

    @staticmethod
    def transpose(matrix):
        output = Matrix(matrix.rows, matrix.cols, None)

        output.values = numpy.transpose(matrix.values).tolist()

        return output

    # Initialize the matrix with values.
    def __init__(self, rows, cols, value=0.0):
        self.rows = rows
        self.cols = cols

        self.values = [[value for col in range(cols)] for row in range(rows)]

    # Multiply the current matrix by a 4-dimensional vector
    def pointVectorMultiply(self, vector):
        outputX = vector.x * self.values[0][0] +\
                    vector.y * self.values[1][0] +\
                    vector.z * self.values[2][0] +\
                    vector.w * self.values[3][0]
        outputY = vector.x * self.values[0][1] +\
                    vector.y * self.values[1][1] +\
                    vector.z * self.values[2][1] +\
                    vector.w * self.values[3][1]
        outputZ = vector.x * self.values[0][2] +\
                    vector.y * self.values[1][2] +\
                    vector.z * self.values[2][2] +\
                    vector.w * self.values[3][2]
        outputW = vector.x * self.values[0][3] +\
                    vector.y * self.values[1][3] +\
                    vector.z * self.values[2][3] +\
                    vector.w * self.values[3][3]
                    
        return Vector(outputX / outputW, outputY / outputW, outputZ / outputW, 1)
        
    def __repr__(self):
        return self.values.__repr__()
