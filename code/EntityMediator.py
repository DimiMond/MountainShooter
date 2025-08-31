from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot

'''''''''
class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:  # if valid_interaction == True:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    #cuidar este código pois se nao funcionar voltar a usar esse e apagar o da linha de baixo
    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)


def verify_health(entity_list: list[Entity]):
    # Primeiro, dá score para inimigos mortos
    for ent in entity_list:
        if ent is not None and ent.health <= 0 and isinstance(ent, Enemy):
            EntityMediator.__give_score(ent, entity_list)

    # Depois, filtra a lista para manter apenas entidades vivas e não-nulas
    entity_list[:] = [
        ent for ent in entity_list
        if ent is not None and ent.health > 0
    ] '''''''''''

#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        # Saiu da janela, mata o enimigo
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        elif isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        elif isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __valid_interaction(ent1: Entity, ent2: Entity) -> bool:
        # PlayerShot ↔ Enemy
        if (isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot)) or \
                (isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy)):
            return True
        # EnemyShot ↔ Player
        if (isinstance(ent1, Player) and isinstance(ent2, EnemyShot)) or \
                (isinstance(ent1, EnemyShot) and isinstance(ent2, Player)):
            return True
        return False

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity):
        # pule entidades já mortas
        if ent1.health <= 0 or ent2.health <= 0:
            return

        if EntityMediator.__valid_interaction(ent1, ent2):
            if ent1.rect.colliderect(ent2.rect):
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
                    break
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score
                    break

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        n = len(entity_list)
        for i in range(n):
            e1 = entity_list[i]
            if e1 is None:
                continue
            EntityMediator.__verify_collision_window(e1)
            for j in range(i + 1, n):
                e2 = entity_list[j]
                if e2 is None:
                    continue
                EntityMediator.__verify_collision_entity(e1, e2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        # Primeiro, dá score para inimigos mortos neste frame
        for ent in entity_list:
            if ent is not None and ent.health <= 0 and isinstance(ent, Enemy):
                EntityMediator.__give_score(ent, entity_list)

        # Depois, filtra mantendo apenas entidades vivas e não-nulas
        entity_list[:] = [ent for ent in entity_list if ent is not None and ent.health > 0]
