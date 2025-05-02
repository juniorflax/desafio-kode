"""
Classes para lidar com itens coletáveis
"""
import math
import random
from pygame.rect import Rect
from constants import TILE_SIZE, YELLOW, GREEN

class Item:
    """Representa os itens coletáveis no jogo (moedas e vidas)"""
    def __init__(self, x, y, item_type):
        self.x = x  # posição x no grid
        self.y = y  # posição y no grid
        self.item_type = item_type  # 'coin' ou 'life'
        self.collected = False  # começa não coletado (obvio né)
        self.animation_time = random.uniform(0, 2)  # pra não ter tudo sincronizado
    
    def update(self, dt):
        # Incrementa o tempo da animação
        self.animation_time += dt
    
    def draw(self, screen):
        # Não desenha se já foi coletado
        if self.collected:
            return
            
        # Efeito flutuante (parece que está levitando)
        offset_y = math.sin(self.animation_time * 3) * 5
        
        # Desenha conforme o tipo do item
        if self.item_type == 'coin':
            # Moeda é um círculo amarelo pulsante
            radius = 6 + math.sin(self.animation_time * 5) * 2  # efeito pulsante
            screen.draw.filled_circle((self.x * TILE_SIZE, self.y * TILE_SIZE + offset_y), radius, YELLOW)
        elif self.item_type == 'life':
            # Vida é um quadrado verde pulsante
            size = 8 + math.sin(self.animation_time * 4) * 2  # efeito pulsante
            rect = Rect(
                self.x * TILE_SIZE - size/2,
                self.y * TILE_SIZE - size/2 + offset_y,
                size,
                size
            )
            screen.draw.filled_rect(rect, GREEN) 