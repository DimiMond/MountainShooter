#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:
            case 'Level1Bg':
                list_bg = []
                for i in range(7):  # level1bg numero de imagens do level 1
                    list_bg.append(Background(f'Level1Bg{i}', (0, 0)))
                    list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
                return list_bg
            case 'Level2Bg':
                list_bg = []
                for i in range(5):  # level2bg numero de imagens do level 2
                    list_bg.append(Background(f'Level2Bg{i}', (0, 0)))
                    list_bg.append(Background(f'Level2Bg{i}', (WIN_WIDTH, 0)))
                return list_bg
            case 'Player1':
                return Player('Player1', (10, WIN_HEIGHT / 2 - 30))
            case 'Player2':
                return Player('Player2', (10, WIN_HEIGHT / 2 + 30))
            case 'Enemy1':
                return Enemy('Enemy1', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
            case 'Enemy2':
                return Enemy('Enemy2', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))


'''''''''
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.Player import Player
from code.PlayerShot import PlayerShot
from code.EnemyShot import EnemyShot
from code.Background import Background

# Caminho base para assets (ajuste se necessário)
BASE_ASSET_PATH = os.path.join(os.path.dirname(__file__), '..', 'Assets')


class EntityFactory:
    @staticmethod
    def get_entity(name: str):
        """
        Cria e retorna uma entidade com base no nome.
        Faz checagem de arquivo e retorna None se não encontrar.
        """
        try:
            # Mapeamento de entidades para construtores e posições iniciais
            mapping = {
                # Inimigos
                'Enemy1': lambda: Enemy('Enemy1', (WIN_WIDTH + 50, WIN_HEIGHT // 4)),
                'Enemy2': lambda: Enemy('Enemy2', (WIN_WIDTH + 50, WIN_HEIGHT // 3)),
                'Enemy3': lambda: Enemy('Enemy3', (WIN_WIDTH + 50, WIN_HEIGHT // 2)),

                # Jogadores
                'Player1': lambda: Player('Player1', (50, WIN_HEIGHT // 2 - 50)),
                'Player2': lambda: Player('Player2', (50, WIN_HEIGHT // 2 + 50)),

                # Tiros
                'Player1Shot': lambda: PlayerShot('Player1Shot', (0, 0)),
                'Player2Shot': lambda: PlayerShot('Player2Shot', (0, 0)),
                'EnemyShot': lambda: EnemyShot('EnemyShot', (0, 0)),

                # Fundos
                'Level1Bg': lambda: [Background('Level1Bg', (0, 0))],
                'Level2Bg': lambda: [Background('Level2Bg', (0, 0))],
                'Level3Bg': lambda: [Background('Level3Bg', (0, 0))],
                'Level1Big': lambda: [Background('Level1Big', (0, 0))],  # seu caso específico
            }

            creator = mapping.get(name)
            if not creator:
                print(f"[EntityFactory] Aviso: entidade '{name}' não está mapeada.")
                return None

            # Antes de criar, checa se o arquivo existe
            asset_file = os.path.join(BASE_ASSET_PATH, f"{name}.png")
            if not os.path.isfile(asset_file):
                print(f"[EntityFactory] ERRO: Arquivo não encontrado -> {asset_file}")
                return None

            return creator()

        except Exception as e:
            print(f"[EntityFactory] Erro ao criar entidade '{name}': {e}")
            return None '''''''''
