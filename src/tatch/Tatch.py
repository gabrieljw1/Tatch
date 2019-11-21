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
        self.timerDelay = 1000//10

        self.terrainLineIdsList = []

        self.cubes = []
        self.cubeLineIdsList = []
        self.cubes.append( Cube(-12,-12,10,-15) )

        self.zStep = 0.0
        self.xStep = 0.0
        self.yStep = 0.0

        self.xShift = 0
        self.zShift = 0

        self.movementSpeed = 0.05

        self.updateTerrain = True

        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)

    def drawTerrain(self):
        terrainVectors = self.world.terrainCache

        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)
        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(terrainVectors)

    def moveCubes(self, dx, dy, dz):
        for cube in self.cubes:
            cube.z += dz
            cube.x0 += dx
            cube.y0 += dy

        cubeRasters = self.generateCubeRasters()

        for i in range(len(cubeRasters)):
            self.tatchFrame.moveCube(cubeRasters[i], self.cubeLineIdsList[i])

    def shiftTerrain(self, dx, dz):
        self.xShift += dx
        self.zShift += dz

        self.world.setTerrainCache(self.world.terrainXOffset,\
                                    self.world.terrainYOffset,\
                                    self.world.terrainZOffset,\
                                    self.xShift,\
                                    self.zShift)

    def moveCamera(self):
        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)

        self.world.moveCamera(self.xStep, self.yStep, self.zStep)

    def drawAll(self, drawTerrain=False):
        if (drawTerrain):
            self.drawTerrain()

    def gameLoop(self):
        startTime = time.time()

        if (self.xStep != 0 or self.yStep != 0 or self.zStep != 0):
            shiftTerrainStart = time.time()
            self.shiftTerrain(self.xStep, self.zStep)
            shiftTerrainEnd = time.time()
            print(f"    shiftTerrain() took {shiftTerrainEnd - shiftTerrainStart}")

            self.updateTerrain = True

        self.drawAll(self.updateTerrain)

        self.updateTerrain = False

        self.after(self.timerDelay, self.gameLoop)

        endTime = time.time()

        print(f"Game loop took {endTime - startTime}s")

    def keyDown(self, event):
        if (event.char == "w"):
            self.zStep = -self.movementSpeed
        elif (event.char == "s"):
            self.zStep = self.movementSpeed

        if (event.char == "a"):
            self.xStep = self.movementSpeed
        elif (event.char == "d"):
            self.xStep = -self.movementSpeed

        if (event.char == "q"):
            self.yStep = self.movementSpeed
        elif (event.char == "e"):
            self.yStep = -self.movementSpeed

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