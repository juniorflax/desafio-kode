"""
Gerenciamento de áudio do jogo
"""
from game_state import game_state
# Imports necessários para o Pygame Zero
import pgzero
from pgzero.builtins import music, sounds

def play_background_music():
    """Toca a música de fundo em loop"""
    try:
        # Pára qualquer música que esteja tocando
        music.stop()
        # Ajusta o volume (0.5 = 50%)
        music.set_volume(0.5)  # nem muito alto nem muito baixo
        # Toca em loop contínuo
        music.play('game_music')  # não precisamos do loop=True, pois é padrão
        print("Tentando tocar música de fundo em loop...")
    except Exception as e:
        # Se der erro, só imprime e continua (não crítico)
        print(f"Erro ao tocar música: {e}")
        # TODO: implementar sistema de fallback para musica

def play_sound(sound_name):
    """Toca um efeito sonoro se o som estiver ligado"""
    if game_state.sound_on:
        try:
            getattr(sounds, sound_name).play()
        except Exception as e:
            print(f"Erro ao tocar som {sound_name}: {e}")

def stop_all_audio():
    """Para toda a reprodução de áudio"""
    try:
        music.stop()
    except Exception as e:
        print(f"Erro ao parar música: {e}") 