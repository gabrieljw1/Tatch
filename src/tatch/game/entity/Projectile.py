from game.entity.Entity import Entity

class Projectile(Entity):
    def __init__(self, entityToWorldMatrix, hitboxVectorList, velocityVector, strength):
        super().__init__(entityToWorldMatrix, hitboxVectorList, velocityVector)
        
        self.strength = strength