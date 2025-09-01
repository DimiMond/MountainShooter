#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from datetime import datetime

from code.DBProxy import DBProxy
from code.Const import C_YELLOW, C_WHITE, SCORE_POS, MENU_OPTION

# Caminho base absoluto
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Score:
    def __init__(self, window: Surface):
        self.window = window

        try:
            img_path = os.path.normpath(os.path.join(BASE_PATH, "..", "asset", "BGscore.png"))
            self.surf = pygame.image.load(img_path).convert_alpha()
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar a imagem BGscore.png: {e}")
            self.surf = Surface((800, 600))  # fallback genérico
            self.surf.fill((0, 0, 0))  # fundo preto

        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        music_path = os.path.normpath(os.path.join(BASE_PATH, "..", "asset", "Score.mp3"))
        try:
            pygame.mixer_music.load(music_path)
            pygame.mixer_music.play(-1)
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar a música Score.mp3: {e}")

        db_proxy = DBProxy('DBScore')
        name = ''

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!!', C_YELLOW, SCORE_POS['Title'])

            text = 'Enter Player 1 name (4 characters):'
            score = player_score[0]

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
            elif game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter Team name (4 characters):'
            elif game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                else:
                    score = player_score[1]
                    text = 'Enter Player 2 name (4 characters):'

            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode

            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])
            pygame.display.flip()

    def show(self):
        music_path = os.path.normpath(os.path.join(BASE_PATH, "..", "asset", "Score.mp3"))
        try:
            pygame.mixer_music.load(music_path)
            pygame.mixer_music.play(-1)
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar a música Score.mp3: {e}")

        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE           DATE      ', C_YELLOW, SCORE_POS['Label'])

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for index, player_score in enumerate(list_score):
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {score:05d}     {date}', C_YELLOW, SCORE_POS[index])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"