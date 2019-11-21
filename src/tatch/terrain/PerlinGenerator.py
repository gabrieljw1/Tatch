import numpy as np
import noise as noise

# The perlin generator generates an [x][y] array populated with terrain heights
#   using perlin noise to create a smooth-ish terrain.
class PerlinGenerator(object):
    def __init__(self, dimensions, scale, octaves=6, persistence=0.5, lacunarity=2.0):
        self.dimensions = dimensions
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def generateGrid(self, xShift, yShift):
        grid = np.zeros(self.dimensions)
        (width, height) = (self.dimensions)

        for x in range(width):
            for y in range(height):
                grid[x][y] = 5*noise.pnoise2((x + xShift)/self.scale,
                                            (y + yShift)/self.scale,
                                            octaves=self.octaves,
                                            persistence=self.persistence,
                                            lacunarity=self.lacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=0)

        return grid