import math

import tkinter as tk
from matrix.Vector import Vector
from matrix.Matrix import Matrix
from engine.Camera import Camera
from World import World
from visual.TatchFrame import TatchFrame
import decimal, random, time

class Tatch(tk.Tk):
    def __init__(self, width=1440, height=900):
        super().__init__()

        self.width = width
        self.height = height

        # Tkinter
        self.tatchFrame = TatchFrame(self, self.width, self.height)


        # Game
        self.world = World( (self.width, self.height) )
        self.timerDelay = 1000//20

        self.terrainLineIdsList = []

        self.zStep = 0.0
        self.xStep = 0.0
        self.yStep = 0.0

        self.xShift = 0.0
        self.zShift = 0.0

        self.movementSpeed = 0.5

        self.updateTerrain = True

        self.backgroundColor = "black"
        self.terrainColor = "white"

        self.tatchFrame.tatchCanvas.config(background=self.backgroundColor)

        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)

    def drawTerrain(self):
        terrainVectors = self.world.terrainCache

        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)
        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(terrainVectors, self.terrainColor)

    def shiftTerrain(self, dx, dz):
        self.xShift += dx
        self.zShift += dz

        self.world.setTerrainCache(self.world.terrainXOffset,\
                                    self.world.terrainYOffset,\
                                    self.world.terrainZOffset,\
                                    self.xShift,\
                                    self.zShift)

    def drawAll(self, drawTerrain=False):
        if (drawTerrain):
            self.drawTerrain()

    def gameLoop(self):
        if (self.xStep != 0 or self.yStep != 0 or self.zStep != 0):
            self.shiftTerrain(self.xStep, self.zStep)

            self.updateTerrain = True

        self.drawAll(self.updateTerrain)

        self.updateTerrain = False

        self.after(self.timerDelay, self.gameLoop)

    def keyDown(self, event):
        if (event.char == "w"):
            self.zStep = self.movementSpeed
        elif (event.char == "s"):
            self.zStep = -self.movementSpeed

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

if __name__ == "__main__":
    tatch = Tatch()
    tatch.after(0, tatch.gameLoop)
    tatch.mainloop()