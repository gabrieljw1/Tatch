import math

import tkinter as tk
from matrix.Vector import Vector
from matrix.Matrix import Matrix
from terrain.TerrainGenerator import TerrainGenerator
from engine.Camera import Camera
import time


########################
# 3D Engine Code
########################

class World(object):
    def __init__(self, imageDims, fieldOfView=90, clippingPlanes=(0.1,100)):
        # Set image and camera variables
        self.imageDims = imageDims
        self.fieldOfView = fieldOfView
        self.clippingPlanes = clippingPlanes

        # Define world axes
        origin = Vector(0, -12, 0)
        xAxis  = Vector(1,0,0)
        yAxis  = Vector(0,1,0)
        zAxis  = Vector(0,0,1)
        self.axes = [origin, xAxis, yAxis, zAxis]

        # Create the camera
        self.camera = Camera(self.fieldOfView,\
                            self.clippingPlanes,\
                            self.imageDims,\
                            self.axes)
        
        # Terrain generation
        self.terrainDims = (77, 30)
        self.terrainScale = 10
        self.terrainXOffset = -39
        self.terrainYOffset = 0
        self.terrainZOffset = 10
        self.terrainGenerator = TerrainGenerator(self.terrainDims,\
                                                self.terrainScale)
        self.terrainCache = self.generateTerrainRasterPoints(self.terrainXOffset, self.terrainYOffset, self.terrainZOffset)

    # Wrapper method for the Terrain Generator's vector generation method.
    # Creates a list of all terrain point vectors.
    def generateTerrainVectors(self, xOffset, yOffset, zOffset, zSign, xShift = 0, yShift = 0):
        return self.terrainGenerator.generateTerrainVectors(xOffset, yOffset, zOffset, zSign, xShift, yShift)

    def generateTerrainRasterPoints(self, xOffset=0, yOffset=0, zOffset=0, xShift = 0, zShift = 0):
        terrainVectors = self.generateTerrainVectors(xOffset, yOffset, zOffset, -1.0, xShift, zShift)

        return [[self.camera.worldToRaster(terrainVectors[x][z], True) for z in range( len(terrainVectors[x]) )] for x in range( len(terrainVectors) )]

    def generateRaster(self, vectors):
        return self.camera.generateRaster(vectors)

    def setTerrainCache(self, xOffset, yOffset, zOffset, xShift, zShift):
        self.terrainCache = self.generateTerrainRasterPoints(xOffset, yOffset, zOffset, xShift, zShift)

    def moveCamera(self, dx, dy, dz):
        origin = self.axes[0]

        self.axes[0] = Vector(origin.x + dx, origin.y + dy, origin.z + dz)

        self.camera = Camera(self.fieldOfView,\
                            self.clippingPlanes,\
                            self.imageDims,\
                            self.axes)

        self.terrainXOffset += dx
        self.terrainYOffset += dy
        self.terrainZOffset += dz

        self.setTerrainCache(self.terrainXOffset, self.terrainYOffset, self.terrainZOffset)
