import math

import tkinter as tk
from game.matrix.Vector import Vector
from game.matrix.Matrix import Matrix
from game.entity.Entity import Entity
from game.entity.Projectile import Projectile
from game.World import World
from game.visual.TatchFrame import TatchFrame
import decimal, random, time
import copy

class Tatch(tk.Tk):
    def __init__(self, width=1440, height=800):
        super().__init__()

        # Set instance variables and create the visual frame
        self.width = width
        self.height = height

        self.tatchFrame = TatchFrame(self, self.width, self.height)


        # View Variables
        fieldOfView = 90
        clippingPlanes = (0.1, 100)
        originVector = Vector(0, -14, 0)
        terrainDims = (54, 29)
        terrainScale = 6.4
        terrainOffsetVector = Vector(0.0, 0.0, 12.0)
        terrainSpread = 1.8

        # Game update variables
        self.paused = False
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



        # Overlay specifications
        self.overlayMargin = 10 # Margin from borders of screen to not draw in
        self.overlayPauseSize = min( self.width // 20, self.height // 20 ) # Side length of pause button (square)
        self.overlayPauseSizeSelectionModifier = 1.4 # How much to expand pause button upon selection

        self.overlayPauseSelected = False
        self.overlayPauseId = None

        self.overlayMenuId = None




        # Bind key event methods
        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)
        self.bind("<Motion>", self.mouseMoved)
        self.bind("<Button>", self.mousePressed)



        # Entities
        self.entities = []

        #player = self.generateEntity(Vector(0, -6, -20), 5)
        enemy = self.generateEntity(Vector(5, -1, -25), 5)

        self.entities.append(enemy)
        self.cubeLineIdsList = []

    def generateEntity(self, positionVector, hitboxRadius):
        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]

        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        hitboxVectorLow = Vector(positionVector.x - hitboxRadius, positionVector.y - hitboxRadius, positionVector.z - hitboxRadius)
        hitboxVectorHigh = Vector(positionVector.x + hitboxRadius, positionVector.y + hitboxRadius, positionVector.z + hitboxRadius)

        return Entity(entityMatrix, [hitboxVectorLow, hitboxVectorHigh])

    def launchProjectile(self, hitboxRadius, velocityVector, damage):
        positionVector = Vector(0,0,0)

        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]

        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        hitboxVectorLow = Vector(positionVector.x - hitboxRadius, positionVector.y - hitboxRadius, positionVector.z - hitboxRadius)
        hitboxVectorHigh = Vector(positionVector.x + hitboxRadius, positionVector.y + hitboxRadius, positionVector.z + hitboxRadius)

        proj = Projectile(entityMatrix, [hitboxVectorLow, hitboxVectorHigh], velocityVector, 10)

        self.entities.append(proj)

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

            if (entity == self.entities[0]):
                color = "red"
            else:
                color = "green"

            cubeIds.extend(self.tatchFrame.drawCube(vertices, color))

        self.cubeLineIdsList = cubeIds

    def drawOverlay(self, pauseButtonSelected):
        #black rectangle,
        #   colored info/settings icon?

        # if selected, make button a little bigger/brighter

        self.tatchFrame.tatchCanvas.delete(self.overlayPauseId)
        self.tatchFrame.tatchCanvas.delete(self.overlayMenuId)

        if (not pauseButtonSelected):
            self.overlayPauseId = self.tatchFrame.tatchCanvas.create_rectangle(self.width - self.overlayMargin,\
                                                        self.overlayMargin,\
                                                        self.width - self.overlayMargin - self.overlayPauseSize,\
                                                        self.overlayMargin + self.overlayPauseSize,\
                                                        fill = "white", outline= "white")
        else:
            self.overlayPauseId = self.tatchFrame.tatchCanvas.create_rectangle(self.width - self.overlayMargin,\
                                                        self.overlayMargin,\
                                                        self.width - self.overlayMargin - self.overlayPauseSizeSelectionModifier*self.overlayPauseSize,\
                                                        self.overlayMargin + self.overlayPauseSizeSelectionModifier*self.overlayPauseSize,\
                                                        fill = "white", outline= "white")

        if (self.paused):
            self.overlayMenuId = self.tatchFrame.tatchCanvas.create_rectangle(self.overlayMargin,\
                                                                                self.overlayMargin,\
                                                                                self.width - self.overlayMargin,\
                                                                                self.height - self.overlayMargin,\
                                                                                fill = "white")

    def drawAll(self, drawTerrain):
        if (drawTerrain):
            self.drawTerrain()
        
        self.drawEntities()
        
        self.drawOverlay(self.overlayPauseSelected)

        if (len(self.entities) > 1):
            if (self.entities[0].collidesWith(self.entities[1])):
                self.pause()

    def gameLoop(self):
        start = time.time()
        for entity in self.entities:
            if (entity.velocityVector != Vector(0,0,0)):
                entity.translate(entity.velocityVector.x, entity.velocityVector.y, entity.velocityVector.z)

            if (isinstance(entity, Projectile) and abs(entity.entityToWorldMatrix.values[3][2]) > 100):
                self.entities.remove(entity)

        if (not self.paused):
            if (self.xStep != 0 or self.yStep != 0 or self.zStep != 0):
                self.shiftTerrain(self.xStep, self.zStep)
                self.entities[0].translate(-self.xStep, self.yStep, self.zStep)

                self.updateTerrain = True
    
        self.drawAll(self.updateTerrain)
        self.updateTerrain = False

        end = time.time()

        if ( (end-start) >= self.timerDelay):
            self.after(end-start + 25, self.gameLoop)
        else:
            self.after(self.timerDelay, self.gameLoop)

    def mouseMoved(self, event):
        if (self.width - self.overlayMargin - self.overlayPauseSize <= event.x \
                and event.x <= self.width - self.overlayMargin\
                and self.overlayMargin <= event.y\
                and event.y <= self.overlayMargin + self.overlayPauseSize):
            self.overlayPauseSelected = True
        else:
            self.overlayPauseSelected = False
    
    def mousePressed(self, event):
        if self.overlayPauseSelected:
            self.pause()

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

        # Launch (for now)
        if (event.char == " "):
            self.launchProjectile(5, Vector(0, 0, -10), 5)

        # Escape
        if (event.char == "\x1b"):
            self.pause()

    def keyUp(self, event):
        if (event.char == "w" or event.char == "s"):
            self.zStep = 0

        if (event.char == "a" or event.char == "d"):
            self.xStep = 0

        if (event.char == "q" or event.char == "e"):
            self.yStep = 0

    def pause(self):
        self.paused = not self.paused

if __name__ == "__main__":
    tatch = Tatch()
    tatch.after(0, tatch.gameLoop)
    tatch.mainloop()