import pyxel as px
from time import time

from src.constants import WIDTH, HEIGHT
from src.game_states import TitleScreen


class Game:
    def __init__(self):
        
        self.score = 0
        self.lives = 3
        self.player =  None #Player(**background_stats["Nakat'th"]['stats'], game=self)
        self.won_game = False
        self.text_timer = 0
        self.text = []

# How to set levels for all sound? Not sure. still not sure
        px.Sound()
        

        self.state = TitleScreen(self)

