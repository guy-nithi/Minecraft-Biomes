"""
Snowflake module :)
Happy New Year
"""
from ursina import Entity, Vec3, time
from random import random

class Flake(Entity):
    sub = None

    @staticmethod
    def setSub(_subjectEntity):
        Flake.sub = _subjectEntity

    def __init__(self,orig):
        super().__init__(
            model='quad',
            texture='flake_1.png',
            position=orig,
            double_sided=True,
            scale=0.2
            )
        self.x+=random()*20-10
        self.z+=random()*20-10
        self.y+=random()*10+5

        minSpeed=1
        self.fallSpeed=random()*4+minSpeed
        minSpin=100
        self.spinSpeed=random()*40+minSpin

    def update(self):
        self.physics()

    def physics(self):
        subPos=Flake.sub.position
        self.y-=self.fallSpeed*time.dt

        self.rotation_y += self.spinSpeed * time.dt
        # Hit ground? If so, respawn above subject.
        if self.y<0:
            self.x=subPos.x+(random()*20-10)
            self.z=subPos.z+(random()*20-10)
            self.y+=subPos.y+(random()*10+5)
            # Would be better to check if we've
            # actually hit a terrain block :|

class SnowFall():
    def __init__(self, _subref):
        self.flakes = []
        Flake.setSub(_subref)
        for i in range(128):
            e = Flake(_subref.position)
            self.flakes.append(e)