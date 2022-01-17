class _Enemy(object):
    
    def __init__(self, health=1, speed=20, cost=1) -> None:
        self.health = health
        self.speed = speed # in pixels per second
        self.cost = cost

    def hit(self, damage=1) -> None:
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self, wallet) -> None:
        wallet += self.cost


class BaseEnemy(_Enemy):
    pass

# Here will be new enemy classes