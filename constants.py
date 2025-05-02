"""
Contém todas as constantes globais do jogo
"""
import pygame.math

# Configurações da tela - ajustar conforme o monitor
SCREEN_WIDTH = 800  # talvez aumente isso depois
SCREEN_HEIGHT = 600  # bom tamanho pra tela atual

# Cores - poderia usar nomes mas prefiro tuplas RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # cor do player
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # moedas
PURPLE = (255, 0, 255)  # inimigo tipo 1
ORANGE = (255, 165, 0)  # inimigo tipo 2, ajustar depois?

# Estados do jogo - usar constantes facilita
MENU = 0      # tela inicial 
PLAYING = 1   # gameplay
GAME_OVER = 2  # game over

# Variáveis do mapa - ajustar se ficar muito grande/pequeno
TILE_SIZE = 40  # 40px parece bom no meu monitor
MAP_WIDTH = 20  # 20 tiles de largura
MAP_HEIGHT = 15   # 15 tiles de altura
