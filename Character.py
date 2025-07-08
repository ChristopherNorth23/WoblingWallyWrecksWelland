class Character:
    
    def __init__(self, strength, speed, weapon, hitpoints, xp, is_alive):
        self.strength = strength
        self.speed = speed
        self.weapon = weapon
        self.hitpoints = hitpoints
        self.max_hitpoints = hitpoints
        self.xp = xp
        self.is_alive = True

    def attack(self):
        """Calculates and returns the damage dealt by the character."""
        return self.strength * -1

    def take_damage(self, damage):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.is_alive = False






