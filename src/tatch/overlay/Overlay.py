class Overlay(object):
    def __init__(self, width, height, tatchCanvas, margin, pauseSize, pauseSizeSelectionModifier, initHealthPoints, initShieldPoints, initAmmoCount):
        self.tatchCanvas = tatchCanvas
        self.width = width
        self.height = height

        self.margin = margin
        self.pauseSize = pauseSize
        self.pauseSizeSelectionModifier = pauseSizeSelectionModifier

        self.initHealthPoints = initHealthPoints
        self.initShieldPoints = initShieldPoints
        self.initAmmoCount    = initAmmoCount

        self.tkinterObjectIds = []

    def clearOverlay(self):
        for tkinterObjectId in self.tkinterObjectIds:
            self.tatchCanvas.delete(tkinterObjectId)

    def drawOverlay(self, pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused, gameIsOver):
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

        # Health, Shield Bar, Ammo Bar
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

        ammoBarBackgroundId = self.tatchCanvas.create_rectangle(self.width - self.margin,\
                                                        self.height - 3*self.margin - 2*self.pauseSize,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - 3*self.margin - 2.5*self.pauseSize,\
                                                        fill = "gray", outline = "black")

        healthBarId = self.tatchCanvas.create_rectangle(self.width - self.margin - (self.initHealthPoints - healthPoints)/self.initHealthPoints*(self.pauseSize*6),\
                                                        self.height - self.margin,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - self.margin - self.pauseSize,\
                                                        fill = "red", outline = "white")

        shieldBarId = self.tatchCanvas.create_rectangle(self.width - self.margin - (self.initShieldPoints - shieldPoints)/self.initShieldPoints*(self.pauseSize*6),\
                                                        self.height - 2*self.margin - self.pauseSize,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - 2*self.margin - 2*self.pauseSize,\
                                                        fill = "blue", outline = "white")

        ammoBarId = self.tatchCanvas.create_rectangle(self.width - self.margin - (self.initAmmoCount - ammoCount)/self.initAmmoCount*(self.pauseSize*6),\
                                                        self.height - 3*self.margin - 2*self.pauseSize,\
                                                        self.width - self.margin - self.pauseSize*6,\
                                                        self.height - 3*self.margin - 2.5*self.pauseSize,\
                                                        fill = "yellow", outline = "white")

        scoreBackgroundId = self.tatchCanvas.create_rectangle(self.margin,\
                                                            self.height - self.margin,\
                                                            self.margin + 6*self.pauseSize,\
                                                            self.height - self.margin - 3*self.pauseSize,\
                                                            fill = "black", outline = "black")

        scoreTextId = self.tatchCanvas.create_text(self.margin + 3*self.pauseSize,\
                                                                    self.height - self.margin - (3/2)*self.pauseSize,\
                                                                    text=f"{score}", fill="white",\
                                                                    font=("Comic Sans", 30))

        # Pause Menu
        if (paused or gameIsOver):
            menuId = self.tatchCanvas.create_rectangle(3 * self.width / 8,\
                                                        3 * self.height / 8,\
                                                        5 * self.width / 8,\
                                                        5 * self.height / 8,\
                                                        fill = "white")

            self.tkinterObjectIds.append( menuId )

            text = "Paused" if paused else "Game Over"

            menuTextId = self.tatchCanvas.create_text(self.width//2,\
                                                    self.height//2,\
                                                    text = text, fill="black",\
                                                    font=("Comic Sans", 30))

            self.tkinterObjectIds.append( menuTextId )

        self.tkinterObjectIds.append( healthBarBackgroundId )
        self.tkinterObjectIds.append( shieldBarBackgroundId )
        self.tkinterObjectIds.append( ammoBarBackgroundId )
        self.tkinterObjectIds.append( healthBarId )
        self.tkinterObjectIds.append( shieldBarId )
        self.tkinterObjectIds.append( ammoBarId )
        self.tkinterObjectIds.append( scoreBackgroundId )
        self.tkinterObjectIds.append( scoreTextId )

    def redrawOverlay(self, pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused, gameIsOver):
        self.clearOverlay()
        self.drawOverlay(pauseButtonSelected, healthPoints, shieldPoints, ammoCount, score, paused, gameIsOver)
