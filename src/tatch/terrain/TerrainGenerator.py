from terrain.PerlinGenerator import PerlinGenerator
from matrix.Vector import Vector

class TerrainGenerator(object):
    def __init__(self, dims, scale):
        self.perlinGenerator = PerlinGenerator(dims, scale)

    def generateTerrainVectors(self, xOffset, yOffset, zOffset, zSign = 1.0, xShift=0, zShift=0):
        perlinGrid = self.perlinGenerator.generateGrid(xShift, zShift)

        terrainVectors = []

        for x in range(len(perlinGrid)):
            row = []

            for z in range(len(perlinGrid[x])):
                y = perlinGrid[x][z]

                row.append( Vector(x + xOffset, y + yOffset, zSign * (z + zOffset)) )

            terrainVectors.append(row)

        return terrainVectors