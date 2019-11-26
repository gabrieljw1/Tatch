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
    def __init__(self, imageDims, fieldOfView, clippingPlanes, originVector, terrainDims, terrainScale, terrainOffsetVector, terrainSpread):
        # Set instance variables
        self.imageDims = imageDims
        self.fieldOfView = fieldOfView
        self.clippingPlanes = clippingPlanes

        # Create the world axes set to define the coordinate system
        xAxis  = Vector(1,0,0)
        yAxis  = Vector(0,1,0)
        zAxis  = Vector(0,0,1)
        self.axes = [originVector, xAxis, yAxis, zAxis]

        # Create the camera
        self.camera = Camera(self.fieldOfView,\
                            self.clippingPlanes,\
                            self.imageDims,\
                            self.axes)

        # Terrain generation
        self.terrainDims = terrainDims
        self.terrainScale = terrainScale
        self.terrainOffsetVector = terrainOffsetVector
        self.terrainSpread = terrainSpread

        self.terrainGenerator = TerrainGenerator(self.terrainDims, self.terrainScale, self.terrainSpread)
        self.terrainCache = self.generateTerrainRasterPoints(self.terrainOffsetVector, -1.0, 0.0, 0.0)

    def generateTerrainRasterPoints(self, terrainOffsetVector, zSign, xShift, zShift):
        terrainVectors = self.terrainGenerator.generateTerrainVectors(terrainOffsetVector, zSign, xShift, zShift)

        return [[self.camera.worldToRaster(terrainVectors[x][z], True) for z in range( len(terrainVectors[x]) )] for x in range( len(terrainVectors) )]

    def setTerrainCache(self, terrainOffsetVector, xShift, zShift):
        self.terrainCache = self.generateTerrainRasterPoints(terrainOffsetVector, -1.0, xShift, zShift)

    def generateRaster(self, vectors):
        return self.camera.generateRaster(vectors)

    def moveCamera(self, dx, dy, dz):
        origin = self.axes[0]

        self.axes[0] = Vector(origin.x + dx, origin.y + dy, origin.z + dz)

        self.camera = Camera(self.fieldOfView,\
                            self.clippingPlanes,\
                            self.imageDims,\
                            self.axes)

        self.terrainOffsetVector.x += dx
        self.terrainOffsetVector.y += dy
        self.terrainOffsetVector.z += dz

        self.setTerrainCache(self.terrainOffsetVector)
