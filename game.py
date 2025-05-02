"""
Lógica principal do jogo
"""
import math
import random
from constants import (
    MENU, PLAYING, GAME_OVER,
    RED, PURPLE, ORANGE, BLUE, GREEN,
    BLACK, WHITE, MAP_WIDTH, MAP_HEIGHT
)
from game_state import game_state
from map import initialize_map
from characters import Player, Enemy
from items import Item
from audio import play_background_music, play_sound, stop_all_audio

def initialize_game():
    """Inicializa/reinicia o jogo - cria o mapa, jogador, inimigos e itens"""
    initialize_map()
    
    # Encontra uma posição válida para o jogador (longe de paredes)
    while True:
        player_x = random.randint(2, MAP_WIDTH-3)  # deixa uma margem de 2 tiles
        player_y = random.randint(2, MAP_HEIGHT-3)
        if game_state.game_map[player_y][player_x] == 0:  # se não for parede
            break
    
    # Cria o jogador
    game_state.player = Player(player_x, player_y)
    
    # Inicializa array de inimigos
    game_state.enemies = []
    # Cores para os diferentes tipos de inimigos
    enemy_colors = [RED, PURPLE, ORANGE, BLUE]  # um pra cada tipo
    
    # Cria 4 inimigos, um de cada tipo
    for i in range(4):
        # Procura posição válida pro inimigo (longe do jogador e de paredes)
        while True:
            enemy_x = random.randint(2, MAP_WIDTH-3)
            enemy_y = random.randint(2, MAP_HEIGHT-3)
            # Verifica se é espaço vazio E se está longe do jogador
            if (game_state.game_map[enemy_y][enemy_x] == 0 and 
                math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2) > 5):
                break
        
        # Adiciona o inimigo à lista
        game_state.enemies.append(Enemy(enemy_x, enemy_y, enemy_colors[i], i))
    
    # Inicializa array de itens
    game_state.items = []
    # Quantidade de itens aumenta com o nível
    for _ in range(5 + game_state.level):  # começa com 6 itens no nível 1
        # Procura posição válida pro item (longe de paredes e outros itens)
        while True:
            item_x = random.randint(2, MAP_WIDTH-3)
            item_y = random.randint(2, MAP_HEIGHT-3)
            if game_state.game_map[item_y][item_x] == 0:  # espaço vazio
                # Verifica se não tem outro item na mesma posição
                if not any(i.x == item_x and i.y == item_y for i in game_state.items):
                    break
        
        # Define o tipo do item (mais moedas que vidas)
        item_type = 'coin' if random.random() < 0.8 else 'life'  # 80% moedas, 20% vidas
        game_state.items.append(Item(item_x, item_y, item_type))
    
    # Inicia a música de fundo se o som estiver ligado
    if game_state.sound_on:
        play_background_music()

def update_menu_state(dt, keyboard):
    """Atualiza o estado do menu"""
    # Lê o estado atual das teclas
    current_up_key = keyboard.up
    current_down_key = keyboard.down
    current_return_key = keyboard.RETURN
    current_space_key = keyboard.space
    
    # Navega pelo menu (cima/baixo)
    if current_up_key and not game_state.prev_up_key:
        game_state.menu_selected = (game_state.menu_selected - 1) % 3  # volta uma opção (com loop)
        play_sound('start')
    elif current_down_key and not game_state.prev_down_key:
        game_state.menu_selected = (game_state.menu_selected + 1) % 3  # avança uma opção (com loop)
        play_sound('start')
    
    # Seleciona a opção atual do menu (Enter ou Espaço)
    if (current_return_key and not game_state.prev_return_key) or (current_space_key and not game_state.prev_space_key):
        # Opção "INICIAR JOGO"
        if game_state.menu_selected == 0:
            game_state.game_state = PLAYING
            initialize_game()
            play_sound('start')
        
        # Opção "SOM: LIGADO/DESLIGADO"
        elif game_state.menu_selected == 1:
            # Inverte o estado do som
            game_state.sound_on = not game_state.sound_on
            if game_state.sound_on:
                play_background_music()
                play_sound('start')
            else:
                stop_all_audio()
        
        # Opção "SAIR"
        elif game_state.menu_selected == 2:
            exit()  # sai do jogo
    
    # Atualiza o estado anterior das teclas para o próximo frame
    game_state.prev_up_key = current_up_key
    game_state.prev_down_key = current_down_key
    game_state.prev_return_key = current_return_key
    game_state.prev_space_key = current_space_key

def update_playing_state(dt, keyboard):
    """Atualiza o estado do jogo durante a gameplay"""
    # Atualiza o jogador
    game_state.player.update(dt, keyboard)
    
    # Atualiza os inimigos e verifica colisão com o jogador
    for enemy in game_state.enemies:
        enemy.update(dt)
        
        # Calcula distância entre jogador e inimigo
        distance = math.sqrt((enemy.x - game_state.player.x)**2 + (enemy.y - game_state.player.y)**2)
        
        # Se colidir com um inimigo e não estiver invulnerável
        if distance < 0.6 and game_state.player.invulnerable <= 0:
            # Perde uma vida
            game_state.lives -= 1
            # Fica invulnerável por 3 segundos
            game_state.player.invulnerable = 3.0
            
            # Se acabaram as vidas, fim de jogo
            if game_state.lives <= 0:
                game_state.game_state = GAME_OVER
                play_sound('game_over')
            else:
                play_sound('hit')
    
    # Atualiza os itens e verifica coleta
    collected_items = 0
    for item in game_state.items:
        item.update(dt)
        
        # Se ainda não foi coletado, verifica distância com o jogador
        if not item.collected:
            distance = math.sqrt((item.x - game_state.player.x)**2 + (item.y - game_state.player.y)**2)
            # Se chegou perto o suficiente, coleta o item
            if distance < 0.7:
                item.collected = True
                
                # Efeitos conforme o tipo do item
                if item.item_type == 'coin':
                    # Moedas dão pontos, aumentando com o nível
                    game_state.score += 10 * game_state.level
                    play_sound('collect')
                elif item.item_type == 'life':
                    # Vida extra (máximo 5)
                    game_state.lives = min(game_state.lives + 1, 5)
                    play_sound('collect')
        
        # Contabiliza itens coletados
        if item.collected:
            collected_items += 1
    
    # Se coletou todos os itens, avança para o próximo nível
    if collected_items == len(game_state.items):
        game_state.level += 1
        initialize_game()  # reinicia com novo nível
        play_sound('level_up')

def update_game_over_state(dt, keyboard):
    """Atualiza o estado do game over"""
    # Lê o estado atual da tecla espaço
    current_space_key = keyboard.space
    
    # Se pressionou espaço, volta para o menu
    if current_space_key and not game_state.prev_space_key:
        game_state.game_state = MENU
        # Reinicia valores para novo jogo
        game_state.score = 0
        game_state.level = 1
        game_state.lives = 3
    
    # Atualiza o estado anterior da tecla espaço
    game_state.prev_space_key = current_space_key 