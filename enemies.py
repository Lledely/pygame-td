class _Enemy(object):
    
    def __init__(self, health: int=1, speed: int=20, cost: int=1) -> None:
        self.health = health
        self.speed = speed # in pixels per second
        self.cost = cost

    def hit(self, damage: int=1) -> None:
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self, wallet: int) -> None:
        wallet += self.cost


class BaseEnemy(_Enemy):
    pass

# Here will be new enemy classes