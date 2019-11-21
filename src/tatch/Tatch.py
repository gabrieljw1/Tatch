import math

import tkinter as tk
from matrix.Vector import Vector
from matrix.Matrix import Matrix
from engine.Camera import Camera
from World import World
from World import Cube
from visual.TatchFrame import TatchFrame
import decimal, random, time

class Tatch(tk.Tk):
    def __init__(self, width=768, height=768):
        super().__init__()

        self.width = width
        self.height = height

        # Tkinter
        self.tatchFrame = TatchFrame(self, self.width, self.height)


        # Game
        self.world = World( (self.width, self.height) )
        self.timerDelay = 1000//1

        self.terrainLineIdsList = []

        self.cubes = []
        self.cubeLineIdsList = []
        self.cubes.append( Cube(-12,-12,10,-15) )

        self.zStep = 0.0
        self.xStep = 0.0
        self.yStep = 0.0

        self.updateTerrain = True

        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)

    def generateCubeRasters(self):
        rasters = []

        for cube in self.cubes:
            rasters.append(self.world.generateRaster(cube.getVectors()))

        return rasters

    def drawTerrain(self):
        terrainVectors = self.world.terrainCache

        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(terrainVectors)

    def drawCubes(self):
        cubeLineIdsList = []

        for raster in self.generateCubeRasters():
            cubeLineIdsList.append(self.tatchFrame.drawCube(raster))

        self.cubeLineIdsList = cubeLineIdsList

    def moveCubes(self, dx, dy, dz):
        for cube in self.cubes:
            cube.z += dz
            cube.x0 += dx
            cube.y0 += dy

        cubeRasters = self.generateCubeRasters()

        for i in range(len(cubeRasters)):
            self.tatchFrame.moveCube(cubeRasters[i], self.cubeLineIdsList[i])

    def moveCamera(self):
        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)

        self.world.moveCamera(self.xStep, self.yStep, self.zStep)

    def drawAll(self, drawTerrain=False):
        if (drawTerrain):
            self.drawTerrain()
        
        if (self.cubeLineIdsList == []):
            self.drawCubes()
        else:
            #self.moveCubes(self.xStep, self.yStep, self.zStep)
            pass

    def gameLoop(self):
        self.updateTerrain = True

        self.drawAll(self.updateTerrain)

        #self.moveCamera()

        self.updateTerrain = False

        self.after(self.timerDelay, self.gameLoop)

    def keyDown(self, event):
        if (event.char == "w"):
            self.zStep = -0.5
        elif (event.char == "s"):
            self.zStep = 0.5

        if (event.char == "a"):
            self.xStep = 0.5
        elif (event.char == "d"):
            self.xStep = -0.5

        if (event.char == "q"):
            self.yStep = 0.5
        elif (event.char == "e"):
            self.yStep = -0.5

    def keyUp(self, event):
        if (event.char == "w" or event.char == "s"):
            self.zStep = 0

        if (event.char == "a" or event.char == "d"):
            self.xStep = 0

        if (event.char == "q" or event.char == "e"):
            self.yStep = 0

tatch = Tatch()
tatch.after(0, tatch.gameLoop)
tatch.mainloop()