from matrix.Vector import Vector
import numpy as np
import noise

class TerrainGenerator(object):
    def __init__(self, dims, scale, pOctaves=6, pPersistence=0.5, pLacunarity=2.0):
        self.dims = dims
        self.scale = scale
        self.pOctaves = pOctaves
        self.pPersistence = pPersistence
        self.pLacunarity = pLacunarity

    def generateGrid(self, xShift, yShift):
        grid = np.zeros(self.dims)
        (width, height) = (self.dims)

        for x in range(width):
            scaledShiftedX = (x + xShift) / self.scale

            for y in range(height):
                grid[x][y] = float(5.0*noise.pnoise2(scaledShiftedX,
                                            (y + yShift)/self.scale,
                                            octaves=self.pOctaves,
                                            persistence=self.pPersistence,
                                            lacunarity=self.pLacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=0))

        return grid

    def generateTerrainVectors(self, xOffset, yOffset, zOffset, zSign = 1.0, xShift=0.0, zShift=0.0):
        perlinGrid = self.generateGrid(xShift, zShift)

        yeet = len(perlinGrid[0])

        return [[ Vector(x + xOffset, perlinGrid[x][z] + yOffset, zSign * (z + zOffset)) for z in range(yeet)] for x in range(len(perlinGrid))]
