#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from pygame.locals import QUIT, KEYDOWN, K_DOWN, K_UP, K_RETURN

from code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW, C_GREEN

# Caminho base absoluto
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Menu:
    def __init__(self, window: Surface):
        self.window = window

        # Caminho para a imagem de fundo
        img_path = os.path.normpath(os.path.join(BASE_PATH, "..", "asset", "BGmenu.png"))
        try:
            self.surf = pygame.image.load(img_path).convert_alpha()
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar BGmenu.png: {e}")
            self.surf = Surface((WIN_WIDTH, 600))
            self.surf.fill((0, 0, 0))  # fundo preto como fallback

        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self) -> str:
        menu_option = 0

        # Caminho para a música
        music_path = os.path.normpath(os.path.join(BASE_PATH, "..", "asset", "Menu.mp3"))
        try:
            pygame.mixer_music.load(music_path)
            pygame.mixer_music.play(-1)
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar Menu.mp3: {e}")

        while True:
            self.window.blit(self.surf, self.rect)
            self.menu_text(50, "Mountain", C_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, "Shooter", C_ORANGE, (WIN_WIDTH / 2, 120))

            for i, option in enumerate(MENU_OPTION):
                color = C_GREEN if i == menu_option else C_WHITE
                self.menu_text(20, option, color, (WIN_WIDTH / 2, 200 + 25 * i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    elif event.key == K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    elif event.key == K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)