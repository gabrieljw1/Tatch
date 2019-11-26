from matrix.Vector import Vector
import numpy as np
import noise
import time

class TerrainGenerator(object):
    def __init__(self, dims, scale, spread, pOctaves=6):
        self.dims = dims
        self.scale = scale
        self.spread = spread
        self.pOctaves = pOctaves

    def generateGrid(self, xShift, yShift):
        grid = np.zeros(self.dims)
        (width, height) = (self.dims)

        scale = self.scale
        octaves = self.pOctaves

        xRange = range(width)
        yRange = range(height)

        for x in xRange:
            scaledShiftedX = (x + xShift) / scale

            for y in yRange:
                grid[x][y] = float(5.0*noise.pnoise2(scaledShiftedX,
                                            (y + yShift)/scale,
                                            octaves=octaves))

        return grid

    def generateTerrainVectors(self, terrainOffsetVector, zSign, xShift, zShift):
        perlinGrid = self.generateGrid(xShift, zShift)

        yank = len(perlinGrid)
        yeet = range(len(perlinGrid[0]))

        offsetX = terrainOffsetVector.x
        offsetY = terrainOffsetVector.y
        offsetZ = terrainOffsetVector.z

        return [[ Vector(self.spread*(x - yank//2) + offsetX, perlinGrid[x][z] + offsetY, (zSign * (self.spread*z + offsetZ))) for z in yeet] for x in range(len(perlinGrid))]
