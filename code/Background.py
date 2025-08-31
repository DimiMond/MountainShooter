#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import WIN_WIDTH, ENTITY_SPEED
from code.Entity import Entity

import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED
from code.Entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple = (0, 0)):
        super().__init__(name, position)

        # Redimensiona a superfície carregada pelo Entity
        self.surf = pygame.transform.scale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        # Atualiza o rect para refletir o novo tamanho e posição inicial
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        # Move para a esquerda
        self.rect.centerx -= ENTITY_SPEED[self.name]

        # Se sair da tela, reposiciona à direita
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
