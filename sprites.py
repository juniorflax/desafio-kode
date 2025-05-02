"""
Classes para lidar com sprites e animações
"""

class AnimatedSprite:
    """Classe pra fazer as animações de sprites
    Nada muito complicado, só muda as cores
    e controla os frames"""
    def __init__(self, base_color, secondary_color=None):
        # TODO: talvez usar imagens no futuro em vez de formas geométricas
        self.base_color = base_color
        # Se não passar cor secundária, usa a mesma da base
        self.secondary_color = secondary_color if secondary_color else base_color
        self.frames = 4  # 4 frames parece bom, testar mais depois
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 0.08  # ~12fps de animação - bom equilíbrio entre fluido e não muito rápido
        
    def update(self, dt):
        # Avança o tempo do frame atual
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            # Passa pro próximo frame e reinicia o tempo
            self.current_frame = (self.current_frame + 1) % self.frames
            self.frame_time = 0
            
    def get_color(self):
        # A cada 2 frames, faz uma mistura das cores pra dar efeito de "piscar"
        if self.current_frame in [1, 3]:  # frames alternados
            # Média das cores pra dar um efeito de "meio termo"
            r = (self.base_color[0] + self.secondary_color[0]) // 2
            g = (self.base_color[1] + self.secondary_color[1]) // 2
            b = (self.base_color[2] + self.secondary_color[2]) // 2
            return (r, g, b)
        return self.base_color  # nos outros frames usa a cor normal 