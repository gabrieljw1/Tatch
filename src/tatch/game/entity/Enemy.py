from game.entity.Entity import Entity
from game.matrix.Vector import Vector

class Enemy(Entity):
    def __init__(self, entityToWorldMatrix, hitboxVectorList, health, projectileStrength, velocityVector = Vector(0,0,0)):
        super().__init__(entityToWorldMatrix, hitboxVectorList, velocityVector)
        
        self.health = health
        self.projectileStrength = projectileStrength