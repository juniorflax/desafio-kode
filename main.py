"""
Arquivo principal de entrada do jogo
"""
import pgzrun
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU, PLAYING, GAME_OVER
from game_state import game_state
from game import (
    update_menu_state, 
    update_playing_state, 
    update_game_over_state
)
from map import draw_map
from ui import draw_menu, draw_hud, draw_game_over
from pgzero.builtins import keyboard

# Configurando o tamanho da janela para o Pygame Zero
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT

def update(dt):
    """Função principal de atualização do jogo - chamada a cada frame"""
    # Limita o delta time para evitar "saltos" com lag
    dt = min(dt, 0.1)  # max 10 FPS efetivos pra física
    
    # Incrementa o tempo da animação global
    game_state.animation_time += dt
    
    # Direciona para a função de update apropriada conforme o estado do jogo
    if game_state.game_state == MENU:
        update_menu_state(dt, keyboard)
    elif game_state.game_state == PLAYING:
        update_playing_state(dt, keyboard)
    elif game_state.game_state == GAME_OVER:
        update_game_over_state(dt, keyboard)

def draw():
    """Função principal de desenho - chamada após cada update"""
    # Desenha conforme o estado atual do jogo
    if game_state.game_state == MENU:
        # Desenha a tela de menu
        draw_menu(screen)
    
    elif game_state.game_state == PLAYING:
        # Limpa a tela
        screen.clear()
        
        # Desenha o mapa (paredes e chão)
        draw_map(screen)
        
        # Desenha os itens não coletados
        for item in game_state.items:
            if not item.collected:
                item.draw(screen)
        
        # Desenha os inimigos
        for enemy in game_state.enemies:
            enemy.draw(screen)
        
        # Desenha o jogador (piscando quando invulnerável)
        if game_state.player.invulnerable <= 0 or math.sin(game_state.animation_time * 10) > 0:
            game_state.player.draw(screen)
        
        # Desenha a interface (pontuação, nível, vidas)
        draw_hud(screen)
    
    elif game_state.game_state == GAME_OVER:
        # Desenha a tela de fim de jogo
        draw_game_over(screen)

# Inicia o jogo!
pgzrun.go()  # essa parte é mágica, é o que faz tudo funcionar :) 