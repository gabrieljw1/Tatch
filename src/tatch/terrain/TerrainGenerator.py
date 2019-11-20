from terrain.PerlinGenerator import PerlinGenerator
from matrix.Vector import Vector

class TerrainGenerator(object):
    def __init__(self, dimensions, scale):
        self.perlinGenerator = PerlinGenerator(dimensions, scale)

    # Generate the terrain vectors from the perlin noise generator. This will
    #   generate a list of vectors according to the dimensions.
    # Note that the horizontal plane in front of the camera is the camera's
    #   $xz$ plane where the $y$ direction is the 'up' and 'down'.
    def generateTerrainVectors(self):
        perlinGrid = self.perlinGenerator.generateGrid()

        terrainVectors = []

        for x in range(len(perlinGrid)):
            for z in range(len(perlinGrid[x])):
                y = perlinGrid[x][z]

                # There must be -z because currently only -z is visible
                # TODO: Make this rely on camera
                terrainVectors.append( Vector(x, y, -z) )

        return terrainVectors

    def generateTerrainVectorSet(self, xOffset=0):
        perlinGrid = self.perlinGenerator.generateGrid()
        
        terrainVectors = []

        for x in range(len(perlinGrid)):
            row = []
            for z in range(len(perlinGrid[x])):
                y = perlinGrid[x][z]

                # There must be -z because currently only -z is visible
                # TODO: Make this rely on camera
                row.append( Vector(x + xOffset, y, -z) )

            terrainVectors.append(row)

        return terrainVectors