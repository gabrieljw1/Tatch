import numpy

from matrix.Vector import Vector

# A matrix object. Self explanatory.
class Matrix(object):
    @staticmethod
    def generateIdentity(rows, cols):
        output = Matrix(rows, cols)

        for row in range(rows):
            for col in range(cols):
                if (row == col):
                    output.values[row][col] = 1

        return output

    # Generate the inverse of a given matrix.
    @staticmethod
    def inverse(matrix):
        output = Matrix(matrix.rows, matrix.cols, None)

        output.values = numpy.linalg.inv( matrix.values ).tolist()

        return output

    # Initialize the matrix with values.
    def __init__(self, rows, cols, value=0):
        self.rows = rows
        self.cols = cols
        
        # Fill all of the values with 0
        values = []

        for row in range(rows):
            rowValues = []
            for col in range(cols):
                rowValues.append(value)

            values.append(rowValues)

        self.values = values

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

        # Since we always want the output to be in cartesian coordinates, not
        #   homogenous coordinates, /w/ must be 1. So normalize if it is not. If
        #   /w/ is 0, then the vector does not exist in cartesian space and must
        #   be voided.
        output = Vector(outputX, outputY, outputZ, outputW)

        if (outputW == 0):
            return None
        elif (outputW != 1):
            return Vector.scalarDivide(output, outputW)
        else:
            return output

    def __repr__(self):
        return self.values.__repr__()
