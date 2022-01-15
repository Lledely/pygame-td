class __Tower(object):
    
    def __init__(self, damage=1, attack_speed=1, attack_range=1) -> _Tower:
        self.damage = damage
        self.attack_speed = attack_speed # in shoots per second
        self.attack_range = attack_range
        
    def deploy(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
    
    def shot(self, target):
        target.hit(self.damage)


class BaseTower(__Tower):
    pass

# Here will be new towers classes