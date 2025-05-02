"""
Gerenciamento do mapa do jogo
"""
import random
from pygame.rect import Rect
from constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, BLACK, WHITE
from game_state import game_state

def initialize_map():
    """Cria o mapa do jogo com paredes e obstáculos aleatórios"""
    # Começa com um mapa vazio (só zeros)
    game_state.game_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # Adiciona paredes nas bordas do mapa (importante pra não sair da tela)
    for x in range(MAP_WIDTH):
        game_state.game_map[0][x] = 1  # parede superior
        game_state.game_map[MAP_HEIGHT-1][x] = 1  # parede inferior
    
    for y in range(MAP_HEIGHT):
        game_state.game_map[y][0] = 1  # parede esquerda
        game_state.game_map[y][MAP_WIDTH-1] = 1  # parede direita
    
    # Adiciona alguns obstáculos aleatórios (não muitos pra não ficar impossível)
    for _ in range(15):  # 15 obstáculos parece bom
        # Tenta posicionar longe das bordas
        x = random.randint(3, MAP_WIDTH-4)
        y = random.randint(3, MAP_HEIGHT-4)
        game_state.game_map[y][x] = 1  # marca como parede
        
        # Às vezes cria um obstáculo em L
        if random.choice([True, False]):  # 50% de chance
            if x+1 < MAP_WIDTH-1: 
                game_state.game_map[y][x+1] = 1  # estende pra direita
            if y+1 < MAP_HEIGHT-1: 
                game_state.game_map[y+1][x] = 1  # estende pra baixo

def draw_map(screen):
    """Desenha o mapa do jogo (parede e chão)"""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            # Cria um retângulo para o tile atual
            rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            # Se for parede (1), desenha um retângulo cinza com borda mais clara
            if game_state.game_map[y][x] == 1:
                # Retângulo externo (mais escuro)
                screen.draw.filled_rect(rect, (120, 120, 120))
                # Retângulo interno (mais claro) - dá um efeito 3D bem simples
                inner_rect = Rect(x * TILE_SIZE + 2, y * TILE_SIZE + 2, 
                                 TILE_SIZE - 4, TILE_SIZE - 4)
                screen.draw.filled_rect(inner_rect, (150, 150, 150))
            else:
                # Se for chão (0), desenha um retângulo cinza escuro
                screen.draw.filled_rect(rect, (50, 50, 50))  # quase preto 