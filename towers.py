from enemies import _Enemy


class __Tower(object):
    
    def __init__(self, damage: int=1, attack_speed: int=1, attack_range: int=1, cost: int = 1) -> None:
        self.damage = damage
        self.attack_speed = attack_speed # in shoots per second
        self.attack_range = attack_range
        self.cost = cost
        
    def deploy(self, x: int=0, y: int=0) -> None:
        self.x = x
        self.y = y
    
    def shot(self, target: _Enemy):
        target.hit(self.damage)


class BaseTower(__Tower):
    pass

# Here will be new towers classes