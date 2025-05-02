"""
Classes de personagens do jogo
"""
import math
import random
from constants import GREEN, BLACK, WHITE, RED, PURPLE, ORANGE, BLUE, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from sprites import AnimatedSprite
from game_state import game_state

class Character:
    """Classe base para personagens do jogo (jogador e inimigos)
    Controla a movimentação, animação e colisão básicas"""
    def __init__(self, x, y, color, speed=0.1):
        self.x = x
        self.y = y
        self.radius = 15  # raio do personagem - 15px fica bom visualmente
        self.speed = speed  # velocidade padrão (baixa)
        self.direction = 'right'  # começa olhando pra direita
        self.moving = False  # começa parado
        # Cria a animação - cor secundária é metade da intensidade da principal
        self.animation = AnimatedSprite(color, (color[0]//2, color[1]//2, color[2]//2))
        self.breathing = 0  # controla o "respiro" do personagem
        
    def update(self, dt):
        # Atualiza animação
        self.animation.update(dt)
        # Incrementa o ciclo de respiração (movimento suave dos olhos)
        self.breathing += dt * 2
        if self.breathing > math.pi * 2:  # completou um ciclo (2π)
            self.breathing = 0
        
    def draw(self, screen):
        # Converte posição de tile para pixels
        pos_x = self.x * TILE_SIZE
        pos_y = self.y * TILE_SIZE
        
        # Pega a cor atual da animação
        color = self.animation.get_color()
        
        # Desenha o corpo (um círculo)
        screen.draw.filled_circle((pos_x, pos_y), self.radius, color)
        
        # Movimento suave dos olhos baseado na respiração
        eye_offset_x = math.sin(self.breathing) * 3
        eye_offset_y = math.cos(self.breathing) * 2
        
        # Desenha os olhos conforme a direção que o personagem está olhando
        if self.direction == 'right':
            # Olho (parte branca)
            screen.draw.filled_circle((pos_x + 5 + eye_offset_x, pos_y - 5 + eye_offset_y), 4, WHITE)
            # Pupila (parte preta)
            screen.draw.filled_circle((pos_x + 5 + eye_offset_x, pos_y - 5 + eye_offset_y), 2, BLACK)
        elif self.direction == 'left':
            screen.draw.filled_circle((pos_x - 5 + eye_offset_x, pos_y - 5 + eye_offset_y), 4, WHITE)
            screen.draw.filled_circle((pos_x - 5 + eye_offset_x, pos_y - 5 + eye_offset_y), 2, BLACK)
        elif self.direction == 'up':
            screen.draw.filled_circle((pos_x + eye_offset_x, pos_y - 8 + eye_offset_y), 4, WHITE)
            screen.draw.filled_circle((pos_x + eye_offset_x, pos_y - 8 + eye_offset_y), 2, BLACK)
        else:  # baixo
            screen.draw.filled_circle((pos_x + eye_offset_x, pos_y + 2 + eye_offset_y), 4, WHITE)
            screen.draw.filled_circle((pos_x + eye_offset_x, pos_y + 2 + eye_offset_y), 2, BLACK)
        
        # Desenha as "pernas" se estiver se movendo
        if self.moving:
            # Calcula o ângulo base dependendo da direção
            base_angle = 0
            if self.direction == 'right':
                base_angle = 0  # 0 radianos = direita
            elif self.direction == 'left':
                base_angle = math.pi  # π radianos = esquerda
            elif self.direction == 'up':
                base_angle = math.pi * 1.5  # 3π/2 radianos = cima
            elif self.direction == 'down':
                base_angle = math.pi * 0.5  # π/2 radianos = baixo
                
            # Animação das pernas - movimento tipo pêndulo
            leg_angle = math.sin(self.animation.current_frame * math.pi) * 0.3
            
            # Calcula posição da primeira perna
            leg_x1 = pos_x + math.cos(base_angle + leg_angle) * 12
            leg_y1 = pos_y + math.sin(base_angle + leg_angle) * 12
            screen.draw.line((pos_x, pos_y), (leg_x1, leg_y1), color)
            
            # Calcula posição da segunda perna (espelhada)
            leg_x2 = pos_x + math.cos(base_angle - leg_angle) * 12
            leg_y2 = pos_y + math.sin(base_angle - leg_angle) * 12
            screen.draw.line((pos_x, pos_y), (leg_x2, leg_y2), color)
    
    def try_move(self, dx, dy):
        """Tenta mover o personagem na direção especificada
        Retorna True se conseguiu mover, False caso contrário"""
        # Calcula nova posição considerando a velocidade
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Verifica se não está tentando sair do mapa
        if new_x < 0.5 or new_x >= MAP_WIDTH - 0.5 or new_y < 0.5 or new_y >= MAP_HEIGHT - 0.5:
            return False
        
        # Converte para coordenadas de tile (inteiras)
        tile_x = int(new_x)
        tile_y = int(new_y)
        
        # Verifica colisão com paredes
        if (tile_x < 0 or tile_x >= MAP_WIDTH or tile_y < 0 or 
            tile_y >= MAP_HEIGHT or game_state.game_map[tile_y][tile_x] == 1):
            # Tenta movimento parcial se for diagonal
            if dx != 0 and dy != 0:
                # Tenta mover só horizontalmente
                new_x_h = self.x + dx * self.speed
                new_y_h = self.y
                tile_x_h = int(new_x_h)
                
                # Tenta mover só verticalmente
                new_x_v = self.x
                new_y_v = self.y + dy * self.speed
                tile_y_v = int(new_y_v)
                
                # Verifica qual movimento parcial é possível
                if (tile_x_h >= 0 and tile_x_h < MAP_WIDTH and 
                    game_state.game_map[int(self.y)][tile_x_h] != 1):
                    # Movimento horizontal é possível
                    self.x = new_x_h
                    self.moving = True
                    
                    # Atualiza direção
                    if dx < 0:
                        self.direction = 'left'
                    else:
                        self.direction = 'right'
                    
                    return True
                elif (tile_y_v >= 0 and tile_y_v < MAP_HEIGHT and 
                      game_state.game_map[tile_y_v][int(self.x)] != 1):
                    # Movimento vertical é possível
                    self.y = new_y_v
                    self.moving = True
                    
                    # Atualiza direção
                    if dy < 0:
                        self.direction = 'up'
                    else:
                        self.direction = 'down'
                    
                    return True
            
            return False # bateu na parede, não pode mover
        
        # Movimento válido, atualiza posição
        self.x, self.y = new_x, new_y
        self.moving = True
        
        # Atualiza a direção que o personagem está olhando
        # Para diagonais, prioriza a maior componente
        if abs(dx) > abs(dy):
            if dx < 0:
                self.direction = 'left'
            elif dx > 0:
                self.direction = 'right'
        else:
            if dy < 0:
                self.direction = 'up'
            elif dy > 0:
                self.direction = 'down'
            
        return True


class Player(Character):
    """Classe do jogador - controlado pelo teclado"""
    def __init__(self, x, y):
        # Jogador é verde e mais rápido que os inimigos padrão
        super().__init__(x, y, GREEN, 0.2)  # velocidade ajustada para novo balanço
        self.invulnerable = 0  # tempo de invulnerabilidade (após levar hit)
    
    def update(self, dt, keyboard):
        super().update(dt)
        
        # Atualiza tempo de invulnerabilidade
        if self.invulnerable > 0:
            self.invulnerable -= dt
        
        # Lê input do teclado
        dx = dy = 0  # delta x e y zerados inicialmente
        if keyboard.left:
            dx = -1  # move pra esquerda
        elif keyboard.right:
            dx = 1   # move pra direita
        
        if keyboard.up:
            dy = -1  # move pra cima
        elif keyboard.down:
            dy = 1   # move pra baixo
        
        # Reseta flag de movimento
        self.moving = False
        # Se tiver alguma direção pressionada, tenta mover
        if dx != 0 or dy != 0:
            self.try_move(dx, dy)


class Enemy(Character):
    """Classe dos inimigos - tem comportamentos diferentes baseados no tipo"""
    def __init__(self, x, y, color, enemy_type):
        # Velocidade mais equilibrada e gradual entre os tipos
        speed = 0.08 + (enemy_type * 0.02)  # reduzida para ser mais suave
        super().__init__(x, y, color, speed)
        self.enemy_type = enemy_type  # 0, 1, 2 ou 3 (diferentes comportamentos)
        # Tempo mais longo entre mudanças de direção para movimentos mais suaves
        self.direction_change_time = random.uniform(1.5, 3.0)
        # Direção atual de movimento (dx, dy)
        self.current_dir = (0, 0)
        # Adiciona interpolação para tornar movimento mais suave
        self.target_dir = (0, 0)  # direção-alvo para interpolar
        self.interpolation_time = 0  # controla a interpolação entre direções
        # Contador de tentativas sucessivas falhas em uma direção
        self.failed_attempts = 0
    
    def check_border_proximity(self):
        """Verifica se o inimigo está próximo da borda do mapa ou de paredes"""
        # Distância mínima desejada das bordas ou paredes
        margin = 2
        
        # Verifica se está próximo da borda do mapa
        if self.x < margin or self.x > MAP_WIDTH - margin or self.y < margin or self.y > MAP_WIDTH - margin:
            return True
            
        # Verifica se existem paredes nas proximidades
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = int(self.x + dx), int(self.y + dy)
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and game_state.game_map[ny][nx] == 1:
                    return True
                    
        return False
    
    def get_center_direction(self):
        """Obtém direção em direção ao centro do mapa"""
        # Cálculo aproximado do centro do mapa
        center_x = MAP_WIDTH / 2
        center_y = MAP_HEIGHT / 2
        
        # Direção para o centro
        dx = center_x - self.x
        dy = center_y - self.y
        
        # Normaliza
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx /= dist
            dy /= dist
            
        return (dx, dy)
    
    def update(self, dt):
        super().update(dt)
        player = game_state.player
        
        # Interpolação suave entre direções
        if self.target_dir != self.current_dir and self.target_dir != (0, 0):
            self.interpolation_time += dt * 2  # velocidade da interpolação
            if self.interpolation_time >= 1.0:
                # Chegou na direção-alvo
                self.current_dir = self.target_dir
                self.interpolation_time = 0
            else:
                # Interpola entre current_dir e target_dir
                factor = self.interpolation_time  # 0.0 até 1.0
                dx_current, dy_current = self.current_dir if self.current_dir != (0, 0) else (0, 0)
                dx_target, dy_target = self.target_dir
                
                # Interpolação linear
                dx_interp = dx_current + (dx_target - dx_current) * factor
                dy_interp = dy_current + (dy_target - dy_current) * factor
                
                # Normaliza o vetor para manter velocidade constante
                length = math.sqrt(dx_interp**2 + dy_interp**2)
                if length > 0:
                    dx_interp /= length
                    dy_interp /= length
                
                # Tenta mover com a direção interpolada
                if self.try_move(dx_interp, dy_interp):
                    self.moving = True
                    self.failed_attempts = 0
                else:
                    self.failed_attempts += 1
                    # Se muitas tentativas falhas, força recálculo da direção
                    if self.failed_attempts > 3:
                        self.direction_change_time = 0
                        self.current_dir = (0, 0)
                        self.target_dir = (0, 0)
                        self.failed_attempts = 0
        # Continua movendo na direção atual se não estiver interpolando
        elif self.current_dir != (0, 0):
            dx, dy = self.current_dir
            if self.try_move(dx, dy):
                self.failed_attempts = 0
            else:
                # Se bateu em algo, recalcula direção imediatamente
                self.direction_change_time = 0
                self.current_dir = (0, 0)
                self.target_dir = (0, 0)
                self.failed_attempts = 0
        
        # Verifica se está preso em uma borda ou parede
        near_border = self.check_border_proximity()
        
        # Decrementa tempo para próxima mudança de direção
        self.direction_change_time -= dt
        
        # Força mudança de direção se estiver preso na borda por muito tempo
        if near_border and self.failed_attempts > 2:
            self.direction_change_time = 0
        
        # Hora de mudar de direção?
        if self.direction_change_time <= 0:
            # Reseta timer com um valor mais longo para movimentos mais suaves
            self.direction_change_time = random.uniform(1.5, 3.0)
            
            # Se estiver próximo da borda, tenta se mover em direção ao centro
            if near_border and random.random() < 0.7:  # 70% de chance de se mover para o centro quando perto de bordas
                self.target_dir = self.get_center_direction()
                if self.current_dir == (0, 0):
                    self.current_dir = self.target_dir
                else:
                    self.interpolation_time = 0
                # Continua com a lógica normal
                
            # Comportamento do inimigo tipo 0: totalmente aleatório, mas evita paredes
            elif self.enemy_type == 0:
                # Escolhe uma direção aleatória - menos diagonais para simplificar
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                           (0.7, 0.7), (-0.7, -0.7)]  # menos diagonais
                
                # Se estiver muito próximo de bordas, prioriza direções que levam ao centro
                if near_border:
                    center_dir = self.get_center_direction()
                    directions.append(center_dir)  # adiciona mais chances de ir ao centro
                    directions.append(center_dir)  # adiciona duas vezes para aumentar probabilidade
                
                # Define a nova direção como alvo para interpolação
                self.target_dir = random.choice(directions)
                if self.current_dir == (0, 0):  # se estiver parado, começa imediatamente
                    self.current_dir = self.target_dir
                else:
                    # Inicia interpolação
                    self.interpolation_time = 0
            
            # Comportamento do inimigo tipo 1: persegue o jogador, mas evita ficar preso
            elif self.enemy_type == 1:
                # Calcula direção para o jogador
                dist_x = player.x - self.x
                dist_y = player.y - self.y
                
                # Normaliza a direção para movimento suave
                dist_total = math.sqrt(dist_x**2 + dist_y**2)
                if dist_total > 0:
                    dx = dist_x / dist_total
                    dy = dist_y / dist_total
                    
                    # Se estiver próximo a bordas, equilibra entre perseguir e ir ao centro
                    if near_border:
                        center_dir_x, center_dir_y = self.get_center_direction()
                        # Mistura direção ao jogador (60%) com direção ao centro (40%)
                        dx = dx * 0.6 + center_dir_x * 0.4
                        dy = dy * 0.6 + center_dir_y * 0.4
                        
                        # Renormaliza
                        dist_total = math.sqrt(dx**2 + dy**2)
                        if dist_total > 0:
                            dx /= dist_total
                            dy /= dist_total
                    
                    # Suaviza a direção para movimentos mais naturais
                    if abs(dx) < 0.2: dx = 0
                    if abs(dy) < 0.2: dy = 0
                    
                    # Renormaliza após ajustes
                    if dx != 0 or dy != 0:
                        dist_total = math.sqrt(dx**2 + dy**2)
                        dx = dx / dist_total
                        dy = dy / dist_total
                        
                        # Define como direção-alvo para interpolação
                        self.target_dir = (dx, dy)
                        if self.current_dir == (0, 0):  # se estiver parado, começa imediatamente
                            self.current_dir = self.target_dir
                        else:
                            # Inicia interpolação
                            self.interpolation_time = 0
                    else:
                        self.target_dir = (0, 0)
                else:
                    self.target_dir = (0, 0)
            
            # Comportamento do inimigo tipo 2: movimento em padrão "quadrado", mas evita paredes
            elif self.enemy_type == 2:
                # Segue um padrão fixo: direita -> baixo -> esquerda -> cima
                directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                index = self.animation.current_frame % 4
                
                # Se estiver perto de bordas/paredes, chance de mudar para direção ao centro
                if near_border and random.random() < 0.6:  # 60% de chance
                    self.target_dir = self.get_center_direction()
                else:
                    # Define como direção-alvo para interpolação
                    self.target_dir = directions[index]
                
                if self.current_dir == (0, 0):  # se estiver parado, começa imediatamente
                    self.current_dir = self.target_dir
                    dx, dy = self.current_dir
                    if not self.try_move(dx, dy):
                        # Se não conseguiu mover, tenta a próxima direção imediatamente
                        if near_border:
                            self.current_dir = self.get_center_direction()
                            self.target_dir = self.current_dir
                        else:
                            index = (index + 1) % 4
                            self.current_dir = directions[index]
                            self.target_dir = self.current_dir
                else:
                    # Inicia interpolação
                    self.interpolation_time = 0
            
            # Comportamento do inimigo tipo 3: foge do jogador, mas evita paredes
            elif self.enemy_type == 3:
                # Calcula direção OPOSTA ao jogador
                dist_x = self.x - player.x
                dist_y = self.y - player.y
                
                # Normaliza a direção para movimento suave
                dist_total = math.sqrt(dist_x**2 + dist_y**2)
                if dist_total > 0:
                    dx = dist_x / dist_total
                    dy = dist_y / dist_total
                    
                    # Se estiver próximo a bordas, equilibra entre fugir e ir ao centro
                    if near_border:
                        center_dir_x, center_dir_y = self.get_center_direction()
                        # Mistura direção oposta ao jogador (50%) com direção ao centro (50%)
                        dx = dx * 0.5 + center_dir_x * 0.5
                        dy = dy * 0.5 + center_dir_y * 0.5
                        
                        # Renormaliza
                        dist_total = math.sqrt(dx**2 + dy**2)
                        if dist_total > 0:
                            dx /= dist_total
                            dy /= dist_total
                    
                    # Adiciona leve aleatoriedade para evitar movimento previsível
                    # Menos aleatoriedade para movimento mais suave
                    dx += random.uniform(-0.2, 0.2)
                    dy += random.uniform(-0.2, 0.2)
                    
                    # Renormaliza após adicionar aleatoriedade
                    dist_total = math.sqrt(dx**2 + dy**2)
                    if dist_total > 0:
                        dx = dx / dist_total
                        dy = dy / dist_total
                        
                        # Define como direção-alvo para interpolação
                        self.target_dir = (dx, dy)
                        if self.current_dir == (0, 0):  # se estiver parado, começa imediatamente
                            self.current_dir = self.target_dir
                        else:
                            # Inicia interpolação
                            self.interpolation_time = 0
                    else:
                        self.target_dir = (0, 0)
                else:
                    self.target_dir = (0, 0) 