import tkinter as tk
from visual.TatchCanvas import TatchCanvas

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
        terrainLineIds = []

        # Iterate over the rhombus strips
        for x in range(len(terrainVectors) - 1):
            for z in range(len(terrainVectors[x]) - 1):
                if (terrainVectors[x][z] is not None and\
                        terrainVectors[x+1][z] is not None and\
                        terrainVectors[x][z+1] is not None):
                    (x0, y0) = terrainVectors[x][z]
                    (x1, y1) = terrainVectors[x+1][z]
                    (x2, y2) = terrainVectors[x][z+1]

                    terrainLineIds.append(self.tatchCanvas.create_line(x0, y0, x1, y1, x2, y2))

        return terrainLineIds

    def clearTerrainLines(self, terrainLineIds):
        for terrainLineId in terrainLineIds:
            self.tatchCanvas.delete(terrainLineId)

    def drawCube(self, raster):
        cubeLineIds = []

        for pos1 in raster:
            for pos2 in raster:
                if (pos1 != pos2):
                    (x1,y1) = pos1
                    (x2,y2) = pos2

                    cubeLineIds.append(self.tatchCanvas.create_line(x1, y1, x2, y2))

        return cubeLineIds

    def moveCube(self, raster, cubeLineIds):
        idIndex = 0

        for pos1 in raster:
            for pos2 in raster:
                if (pos1 != pos2):
                    (x1,y1) = pos1
                    (x2,y2) = pos2

                    self.tatchCanvas.coords(cubeLineIds[idIndex], x1, y1, x2, y2)

                    idIndex += 1
                    