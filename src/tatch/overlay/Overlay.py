class Overlay(object):
    def __init__(self, width, height, tatchCanvas, overlayMargin, overlayPauseSize, overlayPauseSizeModifier):
        self.tatchCanvas = tatchCanvas
        self.width = width
        self.height = height

        self.margin = overlayMargin
        self.pauseSize = overlayPauseSize
        self.pauseSizeSelectionModifier = overlayPauseSizeModifier

        self.tkinterObjectIds = []

    def clearOverlay(self):
        for tkinterObjectId in self.tkinterObjectIds:
            self.tatchCanvas.delete(tkinterObjectId)

    def drawOverlay(self, pauseButtonSelected, healthPoints, ammoCount, score, paused):
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

        if (paused):
            self.tkinterObjectIds.append(self.tatchCanvas.create_rectangle(self.margin,\
                                                                                self.margin,\
                                                                                self.width - self.margin,\
                                                                                self.height - self.margin,\
                                                                                fill = "white"))

        self.tkinterObjectIds.append(self.tatchCanvas.create_text(self.width//2, 20, text=f"Score: {score}", fill="white"))

    def redrawOverlay(self, pauseButtonSelected, healthPoints, ammoCount, score, paused):
        self.clearOverlay()
        self.drawOverlay(pauseButtonSelected, healthPoints, ammoCount, score, paused)
