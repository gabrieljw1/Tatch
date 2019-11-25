from terrain.PerlinGenerator import PerlinGenerator
from matrix.Vector import Vector

class TerrainGenerator(object):
    def __init__(self, dims, scale):
        self.perlinGenerator = PerlinGenerator(dims, scale)

    def generateTerrainVectors(self, xOffset, yOffset, zOffset, zSign = 1.0, xShift=0.0, zShift=0.0):
        perlinGrid = self.perlinGenerator.generateGrid(xShift, zShift)

        yeet = len(perlinGrid[0])

        return [[ Vector(x + xOffset, perlinGrid[x][z] + yOffset, zSign * (z + zOffset)) for z in range(yeet)] for x in range(len(perlinGrid))]
