import math

import tkinter as tk
from game.matrix.Vector import Vector
from game.matrix.Matrix import Matrix
from game.entity.Entity import Entity
from game.entity.Projectile import Projectile
from game.entity.Enemy import Enemy
from game.World import World
from game.visual.TatchFrame import TatchFrame
from overlay.Overlay import Overlay
import decimal, random, time
import copy

class Tatch(tk.Tk):
    def __init__(self, width=1080, height=720):
        # Tkinter initialization
        super().__init__()

        ### User customization

        # User View Variables
        self.fieldOfView            = 90
        self.clippingPlanes         = (0.1, 100)
        self.originVector           = Vector(0, -14, 0)
        self.terrainDims            = (54, 29)
        self.terrainScale           = 6.4
        self.terrainOffsetVector    = Vector(0, 0, 12)
        self.terrainSpread          = 1.8

        # User Gameplay Variables
        self.targetFPS          = 30
        self.movementSpeed      = 1.0
        self.backgroundColor    = "black"
        self.terrainColor       = "white"
        self.enemyColor         = "red"
        self.projectileColor    = "green"
        self.enemySpawnDelay    = 1500
        self.enemyShootDelay    = 500
        self.playerShootTimeout = 50

        self.initAmmoCount      = 20
        self.initHealthPoints   = 100
        self.initShieldPoints   = 25
        self.playerHitboxRadius = 5

        self.projectileHitboxRadius = 1.25
        self.projectileSpeed        = 4
        self.playerProjectileDamage = 18
        self.enemyProjectileDamage  = 15

        ### Game variables

        # Set the instance variables
        self.width = width
        self.height = height

        # Game state
        self.paused        = False
        self.gameIsOver    = False
        self.keysPressed   = set()
        self.score         = 0
        self.ammoCount     = self.initAmmoCount
        self.healthPoints  = self.initHealthPoints
        self.shieldPoints  = self.initShieldPoints
        self.updateTerrain = True
        self.queueProjectileLaunch = False

        # Timing
        self.frameBufferTime  = 25
        self.timerDelay       = 1000 // self.targetFPS
        self.enemySpawnTimer  = 0
        self.enemyShootTimer  = 0
        self.playerShootTimer = 0

        # Drawing, terrain movement, entities
        self.terrainLineIdsList = []
        self.hitboxLineIdsList = []
        self.zStep, self.xStep = 0.0, 0.0
        self.xShift, self.zShift = 0.0, 0.0
        self.entities = []

        # Overlay specifications and state
        self.overlayMargin = 10
        self.overlayPauseSize = min( self.width // 20, self.height // 20 )
        self.overlayPauseSizeSelectionModifier = 1.4
        self.overlayPauseSelected = False

        ### Operations

        # Create the frame, set window pos, set background color, set resizeable
        self.tatchFrame = TatchFrame(self, self.width, self.height)
        self.geometry(str(self.width) + "x" + str(self.height) + "+0+0")
        self.tatchFrame.tatchCanvas.config(background=self.backgroundColor)
        self.resizable(False, False)

        # Create the necessary game objects
        self.world = World( (self.width, self.height), self.fieldOfView, self.clippingPlanes, self.originVector, self.terrainDims, self.terrainScale, self.terrainOffsetVector, self.terrainSpread)
        self.overlay = Overlay(self.width, self.height, self.tatchFrame.tatchCanvas, self.overlayMargin, self.overlayPauseSize, self.overlayPauseSizeSelectionModifier, self.initHealthPoints, self.initShieldPoints, self.initAmmoCount)

        # Bind keyPress/mouse events to their respective functions
        self.bind("<KeyPress>", self.keyDown)
        self.bind("<KeyRelease>", self.keyUp)
        self.bind("<Motion>", self.mouseMoved)
        self.bind("<Button>", self.mousePressed)

        # Create the player entity and spawn the first entity
        self.playerPosition = Vector(self.originVector.x, self.originVector.y/4, self.originVector.z)
        self.playerEntity = self.generateEntity(self.playerPosition, self.playerHitboxRadius)

    
    
    ######
    # Entity Generation (Entity, Projectile, Enemy)
    ######

    # Generate an entity at a given position and hitbox radius.
    def generateEntity(self,positionVector, hitboxRadius):
        # Generate the entity-to-world transformation matrix
        entityAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]
        entityMatrix = Entity.generateEntityToWorldMatrix(entityAxes)

        # Define the hitbox vectors in $Object$ coordinates
        hitboxVectors = [Vector(-hitboxRadius, -hitboxRadius, -hitboxRadius),\
                         Vector(+hitboxRadius, +hitboxRadius, +hitboxRadius)]

        return Entity(entityMatrix, hitboxVectors)

    # Spawn an enemy at a given position and with given attributes
    def spawnEnemy(self, positionVector, hitboxRadius = 5, health = 100, projectileStrength = 10):
        # Generate the entity-to-world transformation matrix
        enemyAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]
        enemyMatrix = Entity.generateEntityToWorldMatrix(enemyAxes)

        # Define the hitbox vectors in $Object$ coordinates
        hitboxVectors = [Vector(-hitboxRadius, -hitboxRadius, -hitboxRadius),\
                         Vector(+hitboxRadius, +hitboxRadius, +hitboxRadius)]

        self.entities.append( Enemy(enemyMatrix, hitboxVectors, health, projectileStrength) )

    # Launch a projectile
    def launchProjectile(self, positionVector, velocityVector, hitboxRadius, damage, launchedByEnemy=False):
        # Generate the projectile-to-world transformation matrix
        projectileAxes = [positionVector, self.world.axes[1], self.world.axes[2], self.world.axes[3]]
        projectileMatrix = Entity.generateEntityToWorldMatrix(projectileAxes)

        # Define the hitbox vectors in $Object$ coordinates
        hitboxVectors = [Vector(-hitboxRadius, -hitboxRadius, -hitboxRadius),\
                         Vector(+hitboxRadius, +hitboxRadius, +hitboxRadius)]

        self.entities.append( Projectile(projectileMatrix, hitboxVectors, velocityVector, damage, launchedByEnemy) )

    # Launch a projectile from another Entity towards the player
    def launchProjectileFromEnemy(self, enemyEntity, hitboxRadius, velocityMagnitude, damage):
        # Get the velocity vector required to hit the player from the entity's
        #   position.
        velocityVector = Vector.getVelocityFromPointToPoint(enemyEntity.getPosition(), self.playerPosition, velocityMagnitude)

        self.launchProjectile(enemyEntity.getPosition(), velocityVector, hitboxRadius, damage, True)



    ######
    # Terrain Movement
    ######

    # Shift the terrain over the X-Z (horizontal) plane and save it in the cache
    def shiftTerrain(self, dx, dz):
        self.xShift += dx
        self.zShift += dz

        self.world.setTerrainCache(self.world.terrainOffsetVector, self.xShift, self.zShift)


    
    ######
    # View Drawing
    ######

    # Clear the terrain lines then redraw from the terrain cache in the world
    def drawTerrain(self):
        self.tatchFrame.clearTerrainLines(self.terrainLineIdsList)
        self.terrainLineIdsList = self.tatchFrame.drawTerrainFromVectors(self.world.terrainCache, self.terrainColor)

    def drawEntityHitboxes(self):
        # Clear all hitboxes on the canvas
        self.tatchFrame.clearTerrainLines(self.hitboxLineIdsList)

        hitboxLineIdsList = []

        for entity in self.entities:
            if entity.visible:
                if ( isinstance(entity, Enemy) ):
                    color = self.enemyColor
                else:
                    color = self.projectileColor

                rasterPoints = self.world.generateRaster( entity.getWorldHitboxVertexVectors() )

                hitboxLineIdsList.extend(self.tatchFrame.drawCube(rasterPoints, color))

        self.hitboxLineIdsList = hitboxLineIdsList

    # Draw all objects
    def drawAll(self, drawTerrain = False, drawHitboxes = False, drawOverlay = False):
        if drawTerrain:
            self.drawTerrain()
        
        if drawHitboxes:
            self.drawEntityHitboxes()

        if drawOverlay:
            self.overlay.redrawOverlay(self.overlayPauseSelected, self.healthPoints, self.shieldPoints, self.ammoCount, self.score, self.paused)        



    ######
    # User Interaction
    ######

    def positionInsidePauseButton(self, x, y):
        return (self.width - self.overlayMargin - self.overlayPauseSize <= x \
                and x <= self.width - self.overlayMargin\
                and self.overlayMargin <= y\
                and y <= self.overlayMargin + self.overlayPauseSize)

    def mouseMoved(self, event):
        self.overlayPauseSelected = self.positionInsidePauseButton(event.x, event.y)

    def mousePressed(self, event):
        if self.overlayPauseSelected:
            self.pause()

    def keyDown(self, event):
        if (event.char == "\x1b"): # Escape
            self.pause()
        elif (event.char == " "): # Space
            self.queueProjectileLaunch = True
        else:
            self.keysPressed.add(event.char)

    def keyUp(self, event):
        if (event.char in self.keysPressed):
            self.keysPressed.remove(event.char)
    


    ######
    # Game State
    ######

    def pause(self):
        self.paused = not self.paused

    def playerHit(self, power):
        if (self.shieldPoints > 0):
            self.shieldPoints -= power

            if (self.shieldPoints < 0):
                self.shieldPoints = 0
        else:
            self.healthPoints -= power

            if (self.healthPoints < 0):
                self.healthPoints = 0

    def gameOver(self):
        self.paused = False
        self.gameIsOver = True


    
    ######
    # Game Loop and Timing
    ######

    def updateTimers(self, timeShift):
        self.enemySpawnTimer  += timeShift
        self.enemyShootTimer  += timeShift
        self.playerShootTimer += timeShift

    def gameLoop(self):
        timeStartGameLoop = time.time()

        if   "w" in self.keysPressed:
            self.zStep = +self.movementSpeed
        elif "s" in self.keysPressed:
            self.zStep = -self.movementSpeed
        else:
            self.zStep = 0

        if   "a" in self.keysPressed:
            self.xStep = +self.movementSpeed
        elif "d" in self.keysPressed:
            self.xStep = -self.movementSpeed
        else:
            self.xStep = 0


        if not self.paused:
            (nearClip, farClip) = self.clippingPlanes
            enemiesExist = False

            # Move terrain
            if (self.xStep != 0 or self.zStep != 0):
                self.shiftTerrain(self.xStep, self.zStep)

                self.updateTerrain = True

            # Launch projectile
            if (self.queueProjectileLaunch and self.playerShootTimer >= self.playerShootTimeout and self.ammoCount > 0):
                self.launchProjectile(self.playerPosition, Vector(0,0,-self.projectileSpeed), self.projectileHitboxRadius, self.playerProjectileDamage)
                self.ammoCount -= 1
                self.playerShootTimer = 0
            elif self.queueProjectileLaunch:
                self.queueProjectileLaunch = False

            for entity in self.entities:
                entityVelocity = entity.velocityVector
                entity.translate(entityVelocity.x - self.xStep, entityVelocity.y, entityVelocity.z + self.zStep)

                if ( abs(entity.entityToWorldMatrix.values[3][2]) > 2 * farClip ): # Despawn condition
                    self.entities.remove(entity)
                elif ( abs(entity.entityToWorldMatrix.values[3][2] > farClip) ): # Not visible condition
                    entity.visible = False
                elif not entity.visible:
                    entity.visible = True

                # Shoot on time if an enemy. If projectile, check collisions
                if isinstance(entity, Enemy):
                    enemiesExist = True
                    if self.enemyShootTimer > self.enemyShootDelay:
                        self.launchProjectileFromEnemy(entity, self.projectileHitboxRadius, self.projectileSpeed, self.enemyProjectileDamage)
                        self.enemyShootTimer = 0
                else:
                    for otherEntity in self.entities:
                        if (entity != otherEntity and not isinstance(otherEntity, Projectile)):
                            if entity.spawnedByEnemy:
                                if entity.collidesWith(self.playerEntity) or self.playerEntity.collidesWith(entity):
                                    self.playerHit(entity.strength)

                                    if entity in self.entities:
                                        self.entities.remove(entity)
                            else:
                                if entity.collidesWith(otherEntity) or otherEntity.collidesWith(entity):
                                    self.entities.remove(otherEntity)
                                    self.entities.remove(entity)

            # If there are no enemies, spawn one
            if not enemiesExist:
                self.spawnEnemy(Vector(random.randint(-15,15), 0, random.randint(-70, -45)))

        # Draw with new information
        self.drawAll(drawTerrain = self.updateTerrain, drawHitboxes = True, drawOverlay = True)
        self.updateTerrain = False

        timeEndGameLoop = time.time()

        timeElapsedGameLoop = timeEndGameLoop-timeStartGameLoop

        # This is necessary just in case the game lags. If the game loop takes
        #   longer than the timer delay, then python will pin the CPU usage at
        #   100 unless a small buffer is added.
        if ( timeElapsedGameLoop >= self.timerDelay):
            self.updateTimers(timeElapsedGameLoop + self.frameBufferTime)
            self.after(timeElapsedGameLoop + self.frameBufferTime, self.gameLoop)
        else:
            self.updateTimers(self.timerDelay)
            self.after(self.timerDelay, self.gameLoop)

if __name__ == "__main__":
    tatch = Tatch()
    tatch.after(0, tatch.gameLoop)
    tatch.mainloop()


# After meeting
#   - Native full screen
#   - Aspect ratio fix
#   - Add more to HUD
#   - Delay between bullet firing so no lag