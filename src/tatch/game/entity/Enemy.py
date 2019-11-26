from game.entity.Entity import Entity

class Enemy(Entity):
    def __init__(self, entityToWorldMatrix, hitboxVectorList, velocityVector, health, projectileStrength):
        super().__init__(entityToWorldMatrix, hitboxVectorList, velocityVector)
        
        self.health = health
        self.projectileStrength = projectileStrength