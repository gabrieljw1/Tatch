import math

import tkinter as tk
from game.matrix.Vector import Vector
from game.matrix.Matrix import Matrix
from game.entity.Entity import Entity
from game.entity.Projectile import Projectile
from game.World import World
from game.visual.TatchFrame import TatchFrame
from overlay.Overlay import Overlay
import decimal, random, time
import copy

class Tatch(tk.Tk):
    # To the TA reading this: here are the controls
    # WASD to move over the terrain
    # Q/E  to change the height of enemies
    # SPACE to shoot (killing an enemy spawns a new one)
    def __init__(self, width=1080, height=720):
        super().__init__()

        # Set instance variables and create the visual frame
        self.width = width
        self.height = height

        self.tatchFrame = TatchFrame(self, self.width, self.height)

        # View Variables
        fieldOfView = 90
        self.clippingPlanes = (0.1, 100)
        originVector = Vector(0, -14, 0)
        terrainDims = (54, 29)
        terrainScale = 6.4
        terrainOffsetVector = Vector(0.0, 0.0, 12.0)
        terrainSpread = 1.8


        # Game update variables
        self.paused = False
        self.timerDelay = 1000//30
        self.keysPressed = set()
        self.movementSpeed = 1.0
        self.backgroundColor = "black"
        self.terrainColor = "white"
        self.alternateTerrainColor = "green"

        self.geometry(str(self.width) + "x" + str(self.height) + "+0+0")
        

        # Create the Game objects
        self.world = World( (self.width, self.height), fieldOfView, self.clippingPlanes, originVector, terrainDims, terrainScale, terrainOffsetVector, terrainSpread)
        self.timerDelay = 1000//30
        self.score = 0

        self.terrainLineIdsList = []

        self.zStep, self.xStep, self.yStep = 0.0, 0.0, 0.0
        self.xShift, self.zShift = 0.0, 0.0

        self.updateTerrain = True

        self.tatchFrame.tatchCanvas.config(background=self.backgroundColor)


        # Player variables
        self.ammoCount = 0
        self.healthPoints = 100


        # Overlay specifications
        self.overlayMargin = 10 # Margin from borders of screen to not draw in
        self.overlayPauseSize = min( self.width // 20, self.height // 20 ) # Side length of pause button (square)
        self.overlayPauseSizeSelectionModifier = 1.4 # How much to expand pause button upon selection

        self.overlay = Overlay(self.width, self.height, self.tatchFrame.tatchCanvas, self.overlayMargin, self.overlayPauseSize, self.overlayPauseSizeSelectionModifier)

        self.overlayPauseSelected = False


        # Bind key event methods
        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)
        self.bind("<Motion>", self.mouseMoved)
        self.bind("<Button>", self.mousePressed)

        self.resizable(False, False)


        # Entities
        self.entities = []

        self.spawnEnemy(Vector(0, 0, -25))
        self.cubeLineIdsList = []

    # Generate an entity at a given position and hitbox radius.
    def generateEntity(self, positionVector, hitboxRadius):
        # Get the entity axes (this format of position/xAxis/yAxis/zAxis) is
        #   constant throughout this program. The xAxis, yAxis, zAxis defines
        #   rotation, reflection, etc. The position defines the translation.
        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]

        # Generate the Entity-To-World transformation matrix from the axes
        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        # Generate the 'low' and 'high' vectors. A 'lower' vector is defined as
        #   the vector whose sum of its components (x,y,z) is the lowest.
        hitboxVectorLow = Vector(positionVector.x - hitboxRadius, positionVector.y - hitboxRadius, positionVector.z - hitboxRadius)
        hitboxVectorHigh = Vector(positionVector.x + hitboxRadius, positionVector.y + hitboxRadius, positionVector.z + hitboxRadius)

        return Entity(entityMatrix, [hitboxVectorLow, hitboxVectorHigh])

    # Launch a projectile from the origin going forward.
    def launchProjectile(self, hitboxRadius, velocityVector, damage):
        # Start at the origin and get the axes
        positionVector = Vector(0,0,0)
        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]
        
        # Generate the Entity-To-World transformation matrix from the axes
        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        # Generate the 'low' and 'high' vectors. A 'lower' vector is defined as
        #   the vector whose sum of its components (x,y,z) is the lowest.
        hitboxVectorLow = Vector(positionVector.x - hitboxRadius, positionVector.y - hitboxRadius, positionVector.z - hitboxRadius)
        hitboxVectorHigh = Vector(positionVector.x + hitboxRadius, positionVector.y + hitboxRadius, positionVector.z + hitboxRadius)

        # Create the projectile and add it to the list.
        proj = Projectile(entityMatrix, [hitboxVectorLow, hitboxVectorHigh], velocityVector, 5)

        self.entities.append(proj)

    def spawnEnemy(self, positionVector):
        enemy = self.generateEntity(positionVector, 5)

        self.entities.append(enemy)

    # Draw the terrain from the terrain cache
    def drawTerrain(self):
        terrainVectors = self.world.terrainCache

        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)
        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(terrainVectors, self.terrainColor)

    # Shift the terrain over the X-Z (horizontal) plane.
    def shiftTerrain(self, dx, dz):
        self.xShift += dx
        self.zShift += dz

        self.world.setTerrainCache(self.world.terrainOffsetVector,\
                                    self.xShift,\
                                    self.zShift)

    # Draw all entity hitboxes
    def drawEntities(self):
        cubeIds = []

        # Clear all cubes that are currently on the canvas
        self.tatchFrame.clearTerrainLines(self.cubeLineIdsList)

        for entity in self.entities:
            vertices = self.world.generateRaster(entity.getWorldHitboxVertexVectors())

            # These colors are included for ease of use when looking at hitboxes
            if (entity == self.entities[0]):
                color = "red"
            else:
                color = "green"

            # Store the TKinter line IDs for clearing later
            cubeIds.extend(self.tatchFrame.drawCube(vertices, color))

        self.cubeLineIdsList = cubeIds

    # Draw all objects
    def drawAll(self, drawTerrain):
        if (drawTerrain):
            self.drawTerrain()
        
        self.drawEntities()
        self.overlay.redrawOverlay(self.overlayPauseSelected, self.healthPoints, self.ammoCount, self.score, self.paused)

    # For use when visualizing a hitbox collision. Swap the terrain color and
    #   its alternate.
    def swapTerrainColors(self):
        self.terrainColor, self.alternateTerrainColor = self.alternateTerrainColor, self.terrainColor

    def gameLoop(self):
        start = time.time()

        # Process keys:
        if ("w" in self.keysPressed):
            self.zStep = self.movementSpeed
        elif ("s"  in self.keysPressed):
            self.zStep = -self.movementSpeed
        else:
            self.zStep = 0

        if ("a" in self.keysPressed):
            self.xStep = self.movementSpeed
        elif ("d" in self.keysPressed):
            self.xStep = -self.movementSpeed
        else:
            self.xStep = 0

        if ("q" in self.keysPressed):
            self.yStep = self.movementSpeed
        elif ("e" in self.keysPressed):
            self.yStep = -self.movementSpeed
        else:
            self.yStep = 0

        if (not self.paused):
            # Move the first entity if WASD is pressed
            if (self.xStep != 0 or self.yStep != 0 or self.zStep != 0):
                self.shiftTerrain(self.xStep, self.zStep)
                if (len(self.entities) > 0):
                    
                    self.entities[0].translate(-self.xStep, self.yStep, self.zStep)

                self.updateTerrain = True

            # Move each entity by their velocity and destroy if they leave the 
            #   viewing area.
            for entity in self.entities:
                if (entity.velocityVector != Vector(0,0,0)):
                    entity.translate(entity.velocityVector.x, entity.velocityVector.y, entity.velocityVector.z)

                (near, far) = self.clippingPlanes

                if (abs(entity.entityToWorldMatrix.values[3][2]) > far):
                    self.entities.remove(entity)

            # Check collisions between the first and second entity
            if (len(self.entities) > 1):
                if (self.entities[0].collidesWith(self.entities[1]) or self.entities[1].collidesWith(self.entities[0])):
                    self.entities = []

                    self.score += 100

                    self.spawnEnemy(Vector(random.randint(-15,15), random.randint(1, 3), random.randint(-35, -25)))

                    self.updateTerrain = True

        # Draw all objects 
        self.drawAll(self.updateTerrain)
        self.updateTerrain = False

        end = time.time()

        # This is necessary just in case the game lags. If the game loop takes
        #   longer than the timer delay, then python will pin the CPU usage at
        #   100 unless a small buffer is added.
        if ( (end-start) >= self.timerDelay):
            self.after(end-start + 25, self.gameLoop)
        else:
            self.after(self.timerDelay, self.gameLoop)

    # Whenever the mouse is moved, check to see if it is over a clickable button
    def mouseMoved(self, event):
        if (self.width - self.overlayMargin - self.overlayPauseSize <= event.x \
                and event.x <= self.width - self.overlayMargin\
                and self.overlayMargin <= event.y\
                and event.y <= self.overlayMargin + self.overlayPauseSize):
            self.overlayPauseSelected = True
        else:
            self.overlayPauseSelected = False
    
    # If the mouse is pressed and it is over an object, call that object's
    #   linked method.
    def mousePressed(self, event):
        if self.overlayPauseSelected:
            self.pause()

    # If a key is pressed, do a certain action. Used for WASD/QE, projectile
    #   launching, pause menu with ESC
    def keyDown(self, event):
        # Escape
        if (event.char == "\x1b"):
            self.pause()
        elif (event.char == " "): # Launch
            self.launchProjectile(1, Vector(0, 0, -4), 5)
        else:
            self.keysPressed.add(event.char)

    # Stop moving if WASD/QE is released
    def keyUp(self, event):
        if (event.char in self.keysPressed):
            self.keysPressed.remove(event.char)

    def pause(self):
        self.paused = not self.paused

if __name__ == "__main__":
    tatch = Tatch()
    tatch.after(0, tatch.gameLoop)
    tatch.mainloop()


# After meeting
#   - Native full screen
#   - Aspect ratio fix
#   - Add more to HUD
#   - Documentation and refactor