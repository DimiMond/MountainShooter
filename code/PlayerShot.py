from code.Const import ENTITY_SPEED
from code.Entity import Entity

'''''''''
class PlayerShot(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx += ENTITY_SPEED[self.name] '''''


#!/usr/bin/python
# -*- coding: utf-8 -*-


class PlayerShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # position = (player.rect.right, player.rect.centery)
        # alinhar o projétil ao "nariz" da nave
        self.rect.left = position[0]
        self.rect.centery = position[1]

    def move(self):
        # mover para a direita (pixels por frame)
        self.rect.centerx += ENTITY_SPEED[self.name]
