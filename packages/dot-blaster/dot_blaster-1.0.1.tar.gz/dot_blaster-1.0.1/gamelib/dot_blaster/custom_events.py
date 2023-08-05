import pygame

GAME_OVER = pygame.event.Event(pygame.USEREVENT, attr1="GAME_OVER")
SCORE_INCREASE = pygame.event.Event(pygame.USEREVENT, attr1="SCORE_INCREASE")
