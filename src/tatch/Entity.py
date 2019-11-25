class Entity(object):
    # Hitbox is a list of 4 vectors that define a cube. They are in object
    #   coordinates. To get them to world coordinates, multiply them by this
    #   object's transformation matrix.
    def __init__(self, positionVector, hitboxVectorList):
        self.positionVector = positionVector
        self.hitboxVectorList = hitboxVectorList

    def collidesWith(self, other):
        pass