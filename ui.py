"""
Funções e classes para interface do usuário
"""
import math
from pygame.rect import Rect
from constants import (
    MENU, PLAYING, GAME_OVER, 
    WHITE, GREEN, BLUE, RED, BLACK,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from game_state import game_state
from game import (
    update_menu_state, 
    update_playing_state, 
    update_game_over_state
)
from map import draw_map

def draw_menu(screen):
    """Desenha a tela do menu principal"""
    # Limpa a tela com fundo preto
    screen.fill(BLACK)
    
    # Título do jogo
    screen.draw.text("AVENTURA ROGUELIKE", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4), fontsize=60, color=WHITE)
    
    # Lista de botões: (texto, cor, posição y)
    buttons = [
        ("INICIAR JOGO", GREEN if game_state.menu_selected == 0 else (100, 200, 100), SCREEN_HEIGHT/2),
        ("SOM: " + ("LIGADO" if game_state.sound_on else "DESLIGADO"), BLUE if game_state.menu_selected == 1 else (100, 100, 200), SCREEN_HEIGHT/2 + 80),
        ("SAIR", RED if game_state.menu_selected == 2 else (200, 100, 100), SCREEN_HEIGHT/2 + 160)
    ]
    
    # Desenha cada botão
    for i, (text, color, y) in enumerate(buttons):
        # Cria o retângulo do botão
        rect = Rect(SCREEN_WIDTH/2 - 150, y - 30, 300, 60)
        # Preenche com a cor (destacada se for o botão selecionado)
        screen.draw.filled_rect(rect, color)
        # Desenha a borda do botão
        screen.draw.rect(rect, WHITE)
        # Escreve o texto do botão
        screen.draw.text(text, center=(SCREEN_WIDTH/2, y), fontsize=30, color=WHITE)
        
        # Se for o botão selecionado, desenha um indicador animado
        if i == game_state.menu_selected:
            # Movimento suave do indicador (vai e volta)
            offset = math.sin(game_state.animation_time * 5) * 10
            # Desenha o ">" animado ao lado do botão selecionado
            screen.draw.text(">", midright=(SCREEN_WIDTH/2 - 160 - offset, y), fontsize=40, color=WHITE)

def draw_hud(screen):
    """Desenha a interface do jogador - pontuação, nível e vidas"""
    # Mostra a pontuação atual (canto superior esquerdo)
    screen.draw.text(f"Pontuação: {game_state.score}", topleft=(10, 10), fontsize=30, color=WHITE)
    
    # Mostra o nível atual (abaixo da pontuação)
    screen.draw.text(f"Nível: {game_state.level}", topleft=(10, 50), fontsize=30, color=WHITE)
    
    # Mostra as vidas como círculos verdes (canto superior direito)
    for i in range(game_state.lives):
        # daria pra usar imagens de coração aqui, mas os círculos ficam legais também
        screen.draw.filled_circle((SCREEN_WIDTH - 30 - i*30, 30), 10, GREEN)

def draw_game_over(screen):
    """Tela de game over - mostra pontuação final"""
    # Fundo preto
    screen.fill(BLACK)
    
    # Texto "FIM DE JOGO" bem grande e vermelho
    screen.draw.text("FIM DE JOGO", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3), fontsize=60, color=RED)
    
    # Pontuação final
    screen.draw.text(f"Pontuação Final: {game_state.score}", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), fontsize=40, color=WHITE)
    
    # Instrução para voltar ao menu
    screen.draw.text("Pressione ESPAÇO para voltar ao menu", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 30), fontsize=30, color=WHITE)
    # TODO: adicionar ranking de melhores pontuações 