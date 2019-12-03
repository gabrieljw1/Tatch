class Overlay(object):
    def __init__(self, width, height, tatchCanvas, margin, pauseSize, pauseSizeSelectionModifier):
        self.tatchCanvas = tatchCanvas
        self.width = width
        self.height = height

        self.margin = margin
        self.pauseSize = pauseSize
        self.pauseSizeSelectionModifier = pauseSizeSelectionModifier

        self.tkinterObjectIds = []

    def clearOverlay(self):
        for tkinterObjectId in self.tkinterObjectIds:
            self.tatchCanvas.delete(tkinterObjectId)

    def drawOverlay(self, pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused):
        # Pause Button
        if (not pauseButtonSelected):
            self.tkinterObjectIds.append(self.tatchCanvas.create_rectangle(self.width - self.margin,\
                                                        self.margin,\
                                                        self.width - self.margin - self.pauseSize,\
                                                        self.margin + self.pauseSize,\
                                                        fill = "white", outline= "white"))
        else:
            self.tkinterObjectIds.append(self.tatchCanvas.create_rectangle(self.width - self.margin,\
                                                        self.margin,\
                                                        self.width - self.margin - self.pauseSizeSelectionModifier*self.pauseSize,\
                                                        self.margin + self.pauseSizeSelectionModifier*self.pauseSize,\
                                                        fill = "white", outline= "white"))

        # Health, Shield Bar
        healthBarBackgroundId = self.tatchCanvas.create_rectangle(self.width - self.margin,\
                                                        self.height - self.margin,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - self.margin - self.pauseSize,\
                                                        fill = "gray", outline = "black")

        shieldBarBackgroundId = self.tatchCanvas.create_rectangle(self.width - self.margin,\
                                                        self.height - 2*self.margin - self.pauseSize,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - 2*self.margin - 2*self.pauseSize,\
                                                        fill = "gray", outline = "black")

        healthBarId = self.tatchCanvas.create_rectangle(self.width - self.margin - (100 - healthPoints)/100*(self.pauseSize*6),\
                                                        self.height - self.margin,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - self.margin - self.pauseSize,\
                                                        fill = "red", outline = "white")

        shieldBarId = self.tatchCanvas.create_rectangle(self.width - self.margin - (100 - shieldPoints)/100*(self.pauseSize*6),\
                                                        self.height - 2*self.margin - self.pauseSize,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - 2*self.margin - 2*self.pauseSize,\
                                                        fill = "blue", outline = "white")

        self.tkinterObjectIds.append( healthBarBackgroundId )
        self.tkinterObjectIds.append( shieldBarBackgroundId )
        self.tkinterObjectIds.append( healthBarId )
        self.tkinterObjectIds.append( shieldBarId )

        # Pause Menu
        if (paused):
            self.tkinterObjectIds.append(self.tatchCanvas.create_rectangle(self.margin,\
                                                                                self.margin,\
                                                                                self.width - self.margin,\
                                                                                self.height - self.margin,\
                                                                                fill = "white"))

        self.tkinterObjectIds.append(self.tatchCanvas.create_text(self.width//2, 20, text=f"Score: {score}", fill="white"))

    def redrawOverlay(self, pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused):
        self.clearOverlay()
        self.drawOverlay(pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused)
