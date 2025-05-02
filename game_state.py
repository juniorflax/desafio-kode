"""
Gerencia o estado global do jogo
"""
from constants import MENU

class GameState:
    """Classe para gerenciar o estado global do jogo"""
    def __init__(self):
        self.game_state = MENU  # começa no menu
        self.sound_on = True   # som ligado por padrão, melhor experiência
        self.score = 0
        self.level = 1       # começa no nivel 1
        self.lives = 3       # 3 vidas padrão, talvez mudar depois
        self.animation_time = 0
        
        # Variáveis para controle do menu
        self.menu_selected = 0  # começa com a primeira opção selecionada
        
        # Variáveis para rastrear o estado anterior das teclas
        # Isso evita que segurar a tecla conte como vários pressionamentos
        self.prev_up_key = False
        self.prev_down_key = False
        self.prev_return_key = False
        self.prev_space_key = False
        
        # Referências para classes do jogo
        self.player = None
        self.enemies = []
        self.items = []
        self.game_map = []

# Cria uma instância global do estado do jogo para ser usada por outros módulos
game_state = GameState()
