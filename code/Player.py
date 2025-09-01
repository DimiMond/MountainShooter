#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import pygame.key
import pygame.mixer
import os

from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.PlayerShot import PlayerShot

# Inicializa o mixer
pygame.mixer.init()

# Caminho absoluto para o som do tiro
try:
    base_path = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(base_path, "..", "asset", "Shot.mp3")

    # Normaliza o caminho para funcionar dentro do .exe
    sound_path = os.path.normpath(sound_path)

    tiro_sound = pygame.mixer.Sound(sound_path)
    tiro_sound.set_volume(0.05)  # volume entre 0.0 (mudo) e 1.0 (máximo)
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o som do tiro: {e}")
    tiro_sound = None  # fallback para evitar crash


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        pressed_key = pygame.key.get_pressed()
        speed = ENTITY_SPEED[self.name]

        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= speed
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += speed
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= speed
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += speed

        if self.shot_delay > 0:
            self.shot_delay -= 1

    def shoot(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_SHOOT[self.name]] and self.shot_delay <= 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            spawn_pos = (self.rect.right, self.rect.centery)
            tiro = PlayerShot(name=f'{self.name}Shot', position=spawn_pos)
            if tiro_sound:
                tiro_sound.play()  # 🔊 toca o som do tiro
            return tiro
        return None