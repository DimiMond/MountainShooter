
import os
from abc import ABC, abstractmethod

import pygame.image

from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


# Caminho base: pasta onde este arquivo está
BASE_PATH = os.path.dirname(__file__)

class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name

        # Caminho para a imagem
        img_path = os.path.join(BASE_PATH, '../asset', name + '.png')
        self.surf = pygame.image.load(img_path).convert_alpha()

        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'

    @abstractmethod
    def move(self):
        pass