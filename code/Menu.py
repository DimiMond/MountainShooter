#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW


# Caminho base: pasta onde este arquivo está
BASE_PATH = os.path.dirname(__file__)

class Menu:
    def __init__(self, window):
        self.window = window

        # Caminho absoluto para a imagem de fundo
        img_path = os.path.join(BASE_PATH, '../asset/MenuBg.png')
        self.surf = pygame.image.load(img_path).convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0

        # Caminho absoluto para a música
        music_path = os.path.join(BASE_PATH, '../asset/Menu.mp3')
        pygame.mixer_music.load(music_path)
        pygame.mixer_music.play(-1)

        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Mountain", C_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, "Shooter", C_ORANGE, (WIN_WIDTH / 2, 120))

            for i, option in enumerate(MENU_OPTION):
                color = C_YELLOW if i == menu_option else C_WHITE
                self.menu_text(20, option, color, (WIN_WIDTH / 2, 200 + 25 * i))

            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)