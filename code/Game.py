'''''''''
import pygame
import sys

# Importa constantes e classes usadas no jogo
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Score import Score
from code.Menu import Menu
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            # Inicia o jogo nos modos possíveis
            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                player_score = [0, 0]  # [Player1, Player2]

                # Nível 1
                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score)

                if level_return:
                    # Nível 2
                    level = Level(self.window, 'Level2', menu_return, player_score)
                    level_return = level.run(player_score)

                    if level_return:
                        score.save(menu_return, player_score)

            # Mostrar pontuações
            elif menu_return == MENU_OPTION[3]:
                score.show()

            # Sair do jogo
            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()

            else:
                pygame.quit()
                sys.exit() '''''

import pygame
import sys
import os
import time

# Importa constantes e classes usadas no jogo
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Score import Score
from code.Menu import Menu
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def mostrar_game_over(self):
        # Caminho absoluto da imagem
        base_path = os.path.dirname(os.path.abspath(__file__))
        imagem_path = os.path.join(base_path, "..", "asset", "GameOver.png")

        try:
            # Tenta carregar e redimensionar a imagem
            imagem_game_over = pygame.image.load(imagem_path)
            imagem_game_over = pygame.transform.scale(imagem_game_over, self.window.get_size())
        except pygame.error as e:
            print("Erro ao carregar imagem de Game Over:", e)
            # Cria uma tela preta com texto como fallback
            imagem_game_over = pygame.Surface(self.window.get_size())
            imagem_game_over.fill((0, 0, 0))
            fonte = pygame.font.SysFont("Arial", 60)
            texto = fonte.render("GAME OVER", True, (255, 0, 0))
            texto_rect = texto.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
            imagem_game_over.blit(texto, texto_rect)

        # Exibe a imagem game over
        self.window.blit(imagem_game_over, (0, 0))
        pygame.display.flip()

        # Espera 5 segundos
        time.sleep(5)

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            # Inicia o jogo nos modos possíveis
            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                player_score = [0, 0]  # [Player1, Player2]

                # Nível 1
                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score)

                if not level_return:
                    self.mostrar_game_over()
                    continue  # volta pro menu

                # Nível 2
                level = Level(self.window, 'Level2', menu_return, player_score)
                level_return = level.run(player_score)

                if not level_return:
                    self.mostrar_game_over()
                    continue  # volta pro menu

                # Se passou os dois níveis
                score.save(menu_return, player_score)

            # Mostrar pontuações
            elif menu_return == MENU_OPTION[3]:
                score.show()

            # Sair do jogo
            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()

            else:
                pygame.quit()
                sys.exit()