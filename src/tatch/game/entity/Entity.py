from game.matrix.Matrix import Matrix
from game.matrix.Vector import Vector

class Entity(object):
    @staticmethod
    def generateEntityToWorldMatrix(axes):
        cameraToWorldMatrix = Matrix.generateIdentity(4,4)

        # x-axis
        cameraToWorldMatrix.values[0][0] = float(axes[1].x)
        cameraToWorldMatrix.values[0][1] = float(axes[1].y)
        cameraToWorldMatrix.values[0][2] = float(axes[1].z)

        # y-axis
        cameraToWorldMatrix.values[1][0] = float(axes[2].x)
        cameraToWorldMatrix.values[1][1] = float(axes[2].y)
        cameraToWorldMatrix.values[1][2] = float(axes[2].z)

        # z-azis
        cameraToWorldMatrix.values[2][0] = float(axes[3].x)
        cameraToWorldMatrix.values[2][1] = float(axes[3].y)
        cameraToWorldMatrix.values[2][2] = float(axes[3].z)

        # origin translation
        cameraToWorldMatrix.values[3][0] = float(axes[0].x)
        cameraToWorldMatrix.values[3][1] = float(axes[0].y)
        cameraToWorldMatrix.values[3][2] = float(axes[0].z)

        return cameraToWorldMatrix

    # Hitbox is a list of 4 vectors that define a cube. They are in object
    #   coordinates. To get them to world coordinates, multiply them by this
    #   object's transformation matrix.
    def __init__(self, entityToWorldMatrix, hitboxVectorList, velocityVector = Vector(0,0,0)):
        if (len(hitboxVectorList) != 2):
            raise Exception("Invalid hitbox vector list length")

        self.entityToWorldMatrix = entityToWorldMatrix
        self.worldToEntityMatrix = Matrix.inverse( self.entityToWorldMatrix )
        self.hitboxVectorList = hitboxVectorList
        self.velocityVector = velocityVector

        self.cachedWorldHitboxVectors = []
        self.cachedEntityHitboxVertexVectors = []
        self.cachedWorldHitboxVertexVectors = []

        self.regenWorldHitboxVectors = True
        self.regenEntityHitboxVertexVectors = True
        self.regenWorldHitboxVertexVectors = True

    def translate(self, dx, dy, dz):
        self.entityToWorldMatrix.values[3][0] += dx
        self.entityToWorldMatrix.values[3][1] += dy
        self.entityToWorldMatrix.values[3][2] += dz

        self.worldToEntityMatrix = Matrix.inverse( self.entityToWorldMatrix )

        self.regenWorldHitboxVectors = True
        self.regenEntityHitboxVertexVectors = True
        self.regenWorldHitboxVertexVectors = True
    
    def getWorldHitboxVectors(self):
        if (not self.regenWorldHitboxVectors):
            return self.cachedWorldHitboxVectors

        output = [self.entityToWorldMatrix.pointVectorMultiply(hitboxVector) for hitboxVector in self.hitboxVectorList]

        self.cachedWorldHitboxVectors = output
        self.regenWorldHitboxVectors = False

        return output

    def getEntityHitboxVertexVectors(self):
        if (not self.regenEntityHitboxVertexVectors):
            return self.cachedEntityHitboxVertexVectors

        minimumVector = min(self.hitboxVectorList)
        maximumVector = max(self.hitboxVectorList)

        hitboxVertexVectors = []

        (x0, y0, z0) = (minimumVector.x, minimumVector.y, minimumVector.z)
        (x1, y1, z1) = (maximumVector.x, maximumVector.y, maximumVector.z)

        for x in (x0, x1):
            for y in (y0, y1):
                for z in (z0, z1):
                    hitboxVertexVectors.append( Vector(x, y, z) )

        self.cachedEntityHitboxVertexVectors = hitboxVertexVectors
        self.regenEntityHitboxVertexVectors = False

        return hitboxVertexVectors

    def getWorldHitboxVertexVectors(self):
        if (not self.regenWorldHitboxVertexVectors):
            return self.cachedWorldHitboxVertexVectors

        entityHitboxVertexVectors = self.getEntityHitboxVertexVectors()

        output = [self.entityToWorldMatrix.pointVectorMultiply(hitboxVertexVector) for hitboxVertexVector in entityHitboxVertexVectors]

        self.cachedWorldHitboxVertexVectors = output
        self.regenWorldHitboxVertexVectors = False

        return output

    def collidesWith(self, other):
        thisWorldHitboxVectors = self.getWorldHitboxVectors()
        otherWorldHitboxVectors = other.getWorldHitboxVectors()

        minOther = min(otherWorldHitboxVectors)
        maxOther = max(otherWorldHitboxVectors)

        minThis  = min(thisWorldHitboxVectors)
        maxThis  = max(thisWorldHitboxVectors)

        collidesX = False
        collidesY = False
        collidesZ = False

        if (minOther.x <= maxThis.x and maxThis.x <= maxOther.x) \
                or (minOther.x <= minThis.x and minThis.x <= maxOther.x):
            collidesX = True

        if (minOther.y <= maxThis.y and maxThis.y <= maxOther.y) \
                or (minOther.y <= minThis.y and minThis.y <= maxOther.y):
            collidesY = True

        if (minOther.z <= maxThis.z and maxThis.z <= maxOther.z) \
                or (minOther.z <= minThis.z and minThis.z <= maxOther.z):
            collidesZ = True

        return collidesX and collidesY and collidesZ
