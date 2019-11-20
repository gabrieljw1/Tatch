import math

import tkinter as tk
from matrix.Vector import Vector
from matrix.Matrix import Matrix
from terrain.TerrainGenerator import TerrainGenerator
from engine.Camera import Camera
import decimal, random, time

########################
# Helper Functions
########################

def roundHalfUp(d):
    roundingOperator = decimal.ROUND_HALF_UP

    roundedDecimal = decimal.Decimal(d).to_integral_value(rounding=rounding)
    return int(roundedDecimal)


########################
# 3D Engine Code
########################

class World(object):
    def __init__(self, width, height):
        # Define Axes
        origin = Vector(0,-10,0)
        xAxis  = Vector(1,0,0)
        yAxis  = Vector(0,1,0)
        zAxis  = Vector(0,0,1)

        self.axes = [origin, xAxis, yAxis, zAxis]


        # Camera variables
        fieldOfView = 90
        clippingPlanes = (0.1, 100)
        self.camera = Camera(fieldOfView, clippingPlanes, (width, height), self.axes)
 

        # Terrain generation
        self.terrainGenerator = TerrainGenerator((25,25), 10)
        self.cachedTerrainRasterArray = self.generateTerrainRasterArray()


        # Miscellaneous instance variables
        self.vectors = []

    # To draw the terrain properly, need an [x][z] list that has the screen points
    def generateTerrainVectors(self):
        return self.terrainGenerator.generateTerrainVectors()

    def generateTerrainRasterArray(self, xOffset = 0):
        terrainVectorSet = self.terrainGenerator.generateTerrainVectorSet(xOffset)

        # Get into a [x][z] -> (screenX, screenY)
        terrainRasterArray = []

        for x in range(len(terrainVectorSet)):
            row = []

            for z in range(len(terrainVectorSet[x])):
                rasterPoint = self.camera.worldToRaster(terrainVectorSet[x][z], False)

                row.append(rasterPoint)
            
            terrainRasterArray.append(row)

        self.cachedTerrainRasterArray = terrainRasterArray

        return terrainRasterArray

    def generateAllVectors(self, additionalVectors=[]):
        vectors = []
        
        vectors.extend( self.generateTerrainVectors() )
        vectors.extend( additionalVectors )

        self.vectors = vectors

    def generateRaster(self):
        return self.camera.generateRaster(self.vectors)

    def generateSimpletonRaster(self, vectors):
        return self.camera.generateRaster(vectors)



########################
# TKinter Conversion
########################

class Cube(object):
    @staticmethod
    def generateCubeVectors(x0, y0, r, z):
        topLeft = Vector(x0, y0, z)
        topRight = Vector(x0, y0 + r, z)
        bottomLeft = Vector(x0 + r, y0, z)
        bottomRight = Vector(x0 + r, y0 + r, z)

        backTopLeft = Vector(x0, y0, z - r)
        backTopRight = Vector(x0, y0 + r, z - r)
        backBottomLeft = Vector(x0 + r, y0, z - r)
        backBottomRight = Vector(x0 + r, y0 + r, z - r)

        cubeVectors = []

        cubeVectors += [topLeft] + [topRight] + [bottomLeft] + [bottomRight]
        cubeVectors += [backTopLeft] + [backTopRight] + [backBottomLeft] + [backBottomRight]

        return cubeVectors

    def __init__(self, x0, y0, r, z=-10):
        self.x0 = x0
        self.y0 = y0
        self.r = r
        self.z = z

    def getVectors(self):
        return Cube.generateCubeVectors(self.x0, self.y0, self.r, self.z)

class TatchCanvas(tk.Canvas):
    def redrawAll(self, canvas):
        System.out.println("yeet")

class TatchFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        self.parent = parent
        self.initUserInterface(width, height)

    def initUserInterface(self, width, height):
        self.parent.geometry(str(width) + "x" + str(height))
        
        self.tatchCanvas = TatchCanvas(width=width, height=height)
        self.tatchCanvas.pack()

    def drawTerrainFromVectors(self, terrainVectors):
        startTime = time.time()
        # Iterate over the triangle strips
        for x in range(len(terrainVectors) - 1):
            for z in range(len(terrainVectors[x]) - 1):
                if (terrainVectors[x][z] is not None and\
                        terrainVectors[x+1][z] is not None and\
                        terrainVectors[x][z+1] is not None):
                    (x0, y0) = terrainVectors[x][z]
                    (x1, y1) = terrainVectors[x+1][z]
                    (x2, y2) = terrainVectors[x][z+1]

                    self.tatchCanvas.create_line(x0, y0, x1, y1, x2, y2)
        print("Drawing terrain took: " + str(time.time() - startTime))

    def drawCube(self, raster):
        for pos1 in raster:
            for pos2 in raster:
                if (pos1 != pos2):
                    (x1,y1) = pos1
                    (x2,y2) = pos2

                    self.tatchCanvas.create_line(x1, y1, x2, y2)

class Tatch(tk.Tk):
    def __init__(self, width=600, height=600):
        super().__init__()

        self.width = width
        self.height = height

        # Tkinter
        self.tatchFrame = TatchFrame(self, self.width, self.height)


        # Game
        self.world = World(self.width, self.height)
        self.timerDelay = 1000//30

        self.cubes = []
        self.cubes.append( Cube(-12,-12,10,-15) )

        self.zStep = -1

    def generateCubeRasters(self):
        rasters = []

        for cube in self.cubes:
            rasters.append(self.world.generateSimpletonRaster(cube.getVectors()))

        return rasters

    def drawTerrain(self):
        terrainVectors = self.world.cachedTerrainRasterArray

        self.tatchFrame.drawTerrainFromVectors(terrainVectors)

    def drawCubes(self):
        for raster in self.generateCubeRasters():
            self.tatchFrame.drawCube(raster)

    def drawAll(self):
        self.drawTerrain()
        #self.drawCubes()

    def gameLoop(self):
        self.drawAll()
        self.after(self.timerDelay, self.gameLoop)

tatch = Tatch()
tatch.after(0, tatch.gameLoop)
tatch.mainloop()


# Detecting collisions
# Moving camera