from time import time, sleep
from abc import ABC, abstractmethod
from random import randint as RI

import pyxel as px

from src.constants import *
from src.utils import *
from src.image_classes import *

class GameState(ABC):
    def __init__(self, game):
        self.game = game
        self._next_state = self
        self.MOUSE_LOCATION = ''
        # self.text_timer = 0
        self.speed = 1.5
        self.time_last_frame = time()
        self.time_since_last_move = 0
        self.dt = 0
        self._is_clicking = False
        self._register_click = False
        self.on_enter()


    @abstractmethod
    def on_enter(self):
        pass


    def update(self): #dt, t = time variables
        self.MOUSE_LOCATION = px.mouse_x, px.mouse_y 

        time_this_frame = time()
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.game.text_timer += self.dt
        self.time_since_last_move += self.dt
        # add sprites to running class list and check to make them move
        if self.time_since_last_move >= 1/self.speed:
            self.time_since_last_move=0
            # for runner in Runners.main:
            #     runner.run()

        

    @abstractmethod
    def draw(self):
        pass

    def clear_layers(self):
        Layer.back = []
        Layer.main = []
        Layer.fore = []
        Interactable.main = []
        Interactable.frozen = []
        Runners.main = []

    def get_next_state(self):
        return self._next_state

    def draw_layers(self):
        # Layer.back.append(self.character_info)
        # Layer.back.append(self.item_info)
        # self.game.player.bag.draw()

        # px.cls(Background.color)
        for item in Layer.back:
            item.draw()
        for item in reversed(Layer.main):
            item.draw()
        for item in Layer.fore:
            item.draw()
    
    def check_mouse_position(self):
        for item in Interactable.main:
            if item.intersects(self.MOUSE_LOCATION):
                item.intersection()

    def draw_hud(self):
        # Score on top right
        score = str(self.game.score)
        x = WIDTH - len(score) * 4 - 1

    def build_buttons(self):
        self.exit = Button(self)
        self.explore = ExploreButton(self)
        Layer.main.append(self.exit)
        Layer.main.append(self.explore)
        Interactable.main.append(self.exit)
        Interactable.main.append(self.explore)

    def build_exit(self):
        self.exit = Button(self)
        Layer.main.append(self.exit)
        Interactable.main.append(self.exit)

    def build_interactables(self, class_instances:list):
        for instance in class_instances:
            Layer.main.append(instance)
            Interactable.main.append(instance)

    def build_sprites(self, class_instances:list):
        for sprite in class_instances:
            Layer.main.append(sprite)

  
        # self.trans_state= self.game._previous_state
        # self.game._previous_state = self._next_state
        # self._next_state = self.trans_state

    # def to_town(self):
    #     self._next_state= TownScreenState(self.game)

    # def end_game(self):
    #     self._next_state = EndGameScreen(self.game)

    def is_clicking(self):
        return self._register_click

    def update_clicking_state(self):
        # If not is clicking and mouse is down update is clicking
        if not self._is_clicking and px.btnr(px.MOUSE_BUTTON_LEFT):
            self._is_clicking = True
            self._register_click = True
        # If is clicking and mouse is down should not register as click
        elif self._is_clicking and px.btnr(px.MOUSE_BUTTON_LEFT):
            self._register_click = False
        # Otherwise if is clicking and mouse is not down set is_clicking to false
        else:
            self._is_clicking = False
            self._register_click = False

    def draw(self):
        self.update_clicking_state()
        # px.cls(0)
        self.draw_layers()
        self.check_mouse_position()
        self.game.player.draw_sidebar()
        self.draw_name()
        self.draw_explorer()
        self.display_text()

    def set_previous_state(self):
        self.game._previous_state = self

    def draw_explorer(self):
        if self.game.player.exploring == True:
            if self.name == "The Underbelly" or self.name == "The Shining Forest":
                if self.game.explored > 0 and self.game.explored < 3:
                    x, y = player_sprite_locations[self.name][0]
                elif self.game.explored >= 3 and self.game.explored < 6:
                    x, y = player_sprite_locations[self.name][1]
                elif self.game.explored >= 6 and self.game.explored < 9:
                    x, y = player_sprite_locations[self.name][2]
                elif self.game.explored >= 9:
                    x, y = player_sprite_locations[self.name][3]
                px.blt(x, y, 2, 8, self.game.player.v, 8, 8, 7)

    def display_text(self):
        if len(self.game.text) > 0:

            # change this to just freeze interacables if there is text, 
            # and unfreeze if there is not. maybe conditional based on whether there are interactables or not.
            
            # self.game.text_timer = 0
            if self.game.text[-1] != Interactable.unfreeze:
                # print('adding unfreeze')
                self.game.text.append(Interactable.unfreeze)

            if self.game.text[0] == Interactable.unfreeze:
                Interactable.unfreeze()
                self.game.text.pop(0)

            else:
                # CombatText(**self.game.text[0])
                pass

class TitleScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        self.bg = Background(**background['title'])
        Layer.back.append(self.bg)

    def check_mouse_position(self):
        if px.btnr(px.MOUSE_BUTTON_LEFT):
            self._next_state = GameScreen(self.game)


    def draw(self):
        self.update_clicking_state()
        # self.draw_layers()
        self.bg.draw()
        self.check_mouse_position()
        px.text(4, 12, f'{px.mouse_x}x/{px.mouse_y}y', 7)
        # self.game.player.draw_sidebar()

class IntroScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        px.cls(0)

    # def check_mouse_position(self):
    #     if px.btnr(px.MOUSE_BUTTON_LEFT):
    #         self._next_state = ClassChoiceScreen(self.game)    

    def draw(self):
        self.update_clicking_state()
        # self.draw_layers()
        self.check_mouse_position()
        # self.game.player.draw_sidebar()


class GameScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        px.cls(0)
        self.bg = Background(**background['game_screen'])
        Layer.back.append(self.bg)

    # def check_mouse_position(self):
    #     if px.btnr(px.MOUSE_BUTTON_LEFT):
    #         self._next_state = ClassChoiceScreen(self.game)    

    def draw(self):
        self.update_clicking_state()
        self.draw_layers()
        self.check_mouse_position()
        # self.game.player.draw_sidebar()