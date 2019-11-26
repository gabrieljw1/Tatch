import math

import tkinter as tk
from matrix.Vector import Vector
from matrix.Matrix import Matrix
from Entity import Entity
from World import World
from visual.TatchFrame import TatchFrame
import decimal, random, time
import copy

class Tatch(tk.Tk):
    def __init__(self, width=1440, height=900):
        super().__init__()

        # Set instance variables and create the visual frame
        self.width = width
        self.height = height

        self.tatchFrame = TatchFrame(self, self.width, self.height)


        # View Variables
        fieldOfView = 90
        clippingPlanes = (0.1, 100)
        originVector = Vector(0, -12, 0)
        terrainDims = (54, 29)
        terrainScale = 6.4
        terrainOffsetVector = Vector(0.0, 0.0, 12.0)
        terrainSpread = 1.8

        # Game update variables
        self.timerDelay = 1000//30
        self.movementSpeed = 1.0
        self.backgroundColor = "black"
        self.terrainColor = "white"

        self.geometry(str(self.width) + "x" + str(self.height) + "+0+0")
        


        # Create the Game objects
        self.world = World( (self.width, self.height), fieldOfView, clippingPlanes, originVector, terrainDims, terrainScale, terrainOffsetVector, terrainSpread)
        self.timerDelay = 1000//30

        self.terrainLineIdsList = []

        self.zStep, self.xStep, self.yStep = 0.0, 0.0, 0.0
        self.xShift, self.zShift = 0.0, 0.0

        self.updateTerrain = True

        self.tatchFrame.tatchCanvas.config(background=self.backgroundColor)



        # Bind key event methods
        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)



        # Entities
        self.entities = []

        player = self.generateEntity(Vector(0, -6, -20), 5)
        enemy = self.generateEntity(Vector(5, -1, -25), 5)

        self.entities = [player, enemy]
        self.cubeLineIdsList = []

    def generateEntity(self, positionVector, hitboxRadius):
        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]

        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        hitboxVectorLow = Vector(positionVector.x - hitboxRadius, positionVector.y - hitboxRadius, positionVector.z - hitboxRadius)
        hitboxVectorHigh = Vector(positionVector.x + hitboxRadius, positionVector.y + hitboxRadius, positionVector.z + hitboxRadius)

        return Entity(entityMatrix, [hitboxVectorLow, hitboxVectorHigh])

    def drawTerrain(self):
        terrainVectors = self.world.terrainCache

        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)
        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(terrainVectors, self.terrainColor)

    def shiftTerrain(self, dx, dz):
        self.xShift += dx
        self.zShift += dz

        self.world.setTerrainCache(self.world.terrainOffsetVector,\
                                    self.xShift,\
                                    self.zShift)

    def drawEntities(self):
        cubeIds = []

        self.tatchFrame.clearTerrainLines(self.cubeLineIdsList)

        for entity in self.entities:
            vertices = self.world.generateRaster(entity.getWorldHitboxVertexVectors())

            cubeIds.extend(self.tatchFrame.drawCube(vertices, "red"))

        self.cubeLineIdsList = cubeIds

    def drawAll(self, drawTerrain):
        if (drawTerrain):
            self.drawTerrain()
            self.drawEntities()

        print( self.entities[0].collidesWith(self.entities[1]) )

    def gameLoop(self):
        start = time.time()
        if (self.xStep != 0 or self.yStep != 0 or self.zStep != 0):
            self.shiftTerrain(self.xStep, self.zStep)
            self.entities[0].translate(self.xStep, self.yStep, self.zStep)

            self.updateTerrain = True

        self.drawAll(self.updateTerrain)

        self.updateTerrain = False
        end = time.time()

        if ( (end-start) >= self.timerDelay):
            self.after(end-start + 25, self.gameLoop)
        else:
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