from time import time, sleep
from abc import ABC, abstractmethod
from random import randint as RI

import pyxel as px

from src.constants import *
from src.utils import *
from src.image_classes import *
from src.player import Player

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
        Layer.fog = []
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
        for item in Layer.fog:
            item.draw()
        for item in reversed(Layer.main):
            item.draw()
        for item in Layer.fore:
            item.draw()
    
    # def check_mouse_position(self):
    #     for item in Interactable.main:
    #         if item.intersects(self.MOUSE_LOCATION):
    #             item.intersection()

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
        # self.check_mouse_position()
        self.game.player.draw_sidebar()
        self.draw_name()
        self.draw_explorer()
        self.display_text()

    def set_previous_state(self):
        self.game._previous_state = self

    # def draw_explorer(self):
    #     if self.game.player.exploring == True:
    #         if self.name == "The Underbelly" or self.name == "The Shining Forest":
    #             if self.game.explored > 0 and self.game.explored < 3:
    #                 x, y = player_sprite_locations[self.name][0]
    #             elif self.game.explored >= 3 and self.game.explored < 6:
    #                 x, y = player_sprite_locations[self.name][1]
    #             elif self.game.explored >= 6 and self.game.explored < 9:
    #                 x, y = player_sprite_locations[self.name][2]
    #             elif self.game.explored >= 9:
    #                 x, y = player_sprite_locations[self.name][3]
    #             px.blt(x, y, 2, 8, self.game.player.v, 8, 8, 7)

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
        self.small_world = Button(self, 16, 80, 1, 56, 8, use="Small World - 10")
        self.medium_world = Button(self, 16, 96, 1, 64, 8, use ="Medium World - 15")
        self.large_world = Button(self, 16, 112, 1, 64, 8, use = "Large World - 20")
        self.start_game = Button(self, WIDTH //2 - 20, HEIGHT// 2, 1, 40, 8, use = "Start Game")
        self.fog_of_war_toggle = Button(self,WIDTH //2 - 20, 112, 1, 64, 8, use = "Fog of War")
        self.fast_doom = Button(self, WIDTH * .7, 80, 1, 64, 8, use = "Hard/Fast Doom")
        self.medium_doom = Button(self, WIDTH * .7, 96, 1, 64, 8, use = "Normal Doom")
        self.slow_doom = Button(self, WIDTH * .7, 112, 1, 64, 8, use = "Easy/Slow Doom")
        self.medium_world.color = 10
        self.fog_of_war_toggle.color = 10
        self.medium_doom.color = 10
        Layer.main.append(self.small_world)
        Layer.main.append(self.medium_world)
        Layer.main.append(self.large_world)
        Layer.main.append(self.start_game)
        Layer.main.append(self.fog_of_war_toggle)
        Layer.main.append(self.fast_doom)
        Layer.main.append(self.medium_doom)
        Layer.main.append(self.slow_doom)

        for item in Layer.main:
            Interactable.main.append(item)




    def check_mouse_position(self):
        if px.btnr(px.MOUSE_BUTTON_LEFT):
            for button in Interactable.main:
                if button.intersects(self.MOUSE_LOCATION):
                    if button.use == "Small World - 10":
                        self.game.size = 10
                        self.small_world.color = 10
                        self.medium_world.color = 13
                        self.large_world.color = 13

                    elif button.use == "Medium World - 15":
                        self.game.size = 15
                        self.small_world.color = 13
                        self.medium_world.color = 10
                        self.large_world.color = 13

                    elif button.use == "Large World - 20":
                        self.game.size = 20
                        self.small_world.color = 13
                        self.medium_world.color = 13
                        self.large_world.color = 10

                    elif button.use == "Start Game":
                        self._next_state = GameScreen(self.game)
                    elif button.use == "Fog of War":
                        if self.game.fog == True:
                            self.game.fog = False
                            self.fog_of_war_toggle.color = 13
                        else:
                            self.game.fog = True
                            self.fog_of_war_toggle.color = 10
                        
                    elif button.use == "Hard/Fast Doom":
                        self.game.doom_speed = 8
                        self.fast_doom.color = 10
                        self.medium_doom.color = 13
                        self.slow_doom.color = 13

                    elif button.use == "Normal Doom":
                        self.game.doom_speed = 16
                        self.fast_doom.color = 13
                        self.medium_doom.color = 10
                        self.slow_doom.color = 13

                    elif button.use == "Easy/Slow Doom":
                        self.game.doom_speed = 32
                        self.fast_doom.color = 13
                        self.medium_doom.color = 13
                        self.slow_doom.color = 10




    def draw(self):
        self.update_clicking_state()
        # self.draw_layers()
        # self.bg.draw()
        self.draw_layers()
        self.check_mouse_position()
        # px.text(4, 12, f'{px.mouse_x}x/{px.mouse_y}y', 7)

        # px.text(16, 32, "Small World - 10", 7)
        # px.text(16, 48, "Medium World - 15", 7)
        # px.text(16, 64, "Large World - 20", 7)
        # px.text(200, 16, f'{self.game.size}', 7)
        # px.text(WIDTH //2 - 20, HEIGHT// 2, "Start Game", 8)

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
        # self.check_mouse_position()
        # self.game.player.draw_sidebar()


class GameScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        px.cls(0)
        # self.bg = Background(**background['game_screen'])
        # Layer.back.append(self.bg)
        if self.game.size == 10:
            self.start = 56
        elif self.game.size == 15:
            self.start = 16
        elif self.game.size >= 20:
            self.start = 0
        self.generate_map(self.game.size, self.start)
        # self.generate_fog(self.game.size * 4, self.start)
        self.game.player = Player(player_sprite_u_v['front'][0], player_sprite_u_v["front"][1], Layer.fog, self.start) # 
        Layer.main.append(self.game.player)

        self.player_action_count = 0
        self.encroaching_dooms_count = 0
        # self.game.player.move()


    # def check_mouse_position(self):
    #     if px.btnr(px.MOUSE_BUTTON_LEFT):
    #         self._next_state = ClassChoiceScreen(self.game)    

    def draw(self):
        self.update_clicking_state()
        self.draw_layers()
        self.check_player_location()
        # self.check_sight()
        px.text(4, 12, f'{px.mouse_x}x/{px.mouse_y}y', 7)
        px.text(200, 16, f'{self.encroaching_dooms_count}', 7)
        px.text(200, 24, f'{self.player_action_count}', 7)


    def generate_map(self, size=20, start=0):
        self.map = [[0]* size for i in range(size)]
        # generate size - 1 number of numbers between 0 and 4.

        for i in range(size):
            for j in range(10):
                self.map[i][j] = RI(0, 4)

        # insert 5 into the map at a random location
        self.map[RI(size//2, size-1)][RI(0, 9)] = 5

        # for each element of the map create a tile whose u and v values are determined by the number in the map, whose x value starts at self.start and increases by 16 for each element in the row, and whose y values increase by 16 for each element in the column and append the Tile object to Layer.back.
        for i in range(size):
            for j in range(10):
                Layer.back.append(Tile(tile_list_u_v[self.map[i][j]][0], tile_list_u_v[self.map[i][j]][1], 0, start + i*16, j*16, column=i))
        
        for tile in Layer.back:
            Interactable.main.append(tile)


    def generate_fog(self, size=20, start=0):
        self.fog = [[0]* size for i in range(size)]

        for i in range(size):
            for j in range(40):
                Layer.fog.append(Tile(fog_u_v[0], fog_u_v[1], 0, start + i*4, j*4, 4, 4))
        # Layer.fore.append(px.text(200, 32, f'{self.fog}', 7))

    def check_player_location(self):
        for tile in Interactable.main:
            if (tile.x >= self.game.player.x - 12 and 
                tile.x <= self.game.player.x + 4 and 
                tile.y <= self.game.player.y + 8 and 
                tile.y >= self.game.player.y - 8):

                """ 32 >= 24+7 (py +7)
                32 <= 38+7
                32 > = """
                if tile.name == "Cave":
                    self._next_state = WinScreen(self.game)
                elif tile.name == "Encroaching Doom":
                    self._next_state = LoseScreen(self.game)
                else:
                    self.game.player.adjusted_speed = self.game.player.speed * tile.intersection()
                    px.text(200, 32, f'intersect', 7)
                    px.text(200, 40, f'{tile.name}', 7)
                    

    def death_comes(self):
        if self.player_action_count >= self.game.doom_speed:
            self.encroaching_dooms_count += 1
            self.player_action_count = 0
            for i in range(9,-1, -1):
                Layer.back[i].name = "Encroaching Doom"
                Layer.back.remove(Layer.back[i])
            
    def update(self):
        if self.game.player.move() == 1:
            self.player_action_count += 1
        self.death_comes()

class WinScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        px.cls(0)
        self.bg = Background(**background['game_screen'])
        Layer.back.append(self.bg)
        self.game.player = Player(player_sprite_u_v['front'][0], player_sprite_u_v["front"][1], Layer.fog, 120, 80) # 
        Layer.main.append(self.game.player)
        # self.game.player.move()

    def draw(self):
        self.update_clicking_state()
        self.draw_layers()
        self.check_mouse_position()
        px.text(140, 70, f'You Won!', 7)
        px.text(140, 80, f'Click to play again', 7)


    def check_mouse_position(self):
        if px.btnr(px.MOUSE_BUTTON_LEFT):
            self._next_state = TitleScreen(self.game)

class LoseScreen(GameState):
    def on_enter(self):
        self.clear_layers()
        px.cls(0)
        self.bg = Background(**background['game_screen'])
        Layer.back.append(self.bg)


    def draw(self):
        self.update_clicking_state()
        self.draw_layers()
        self.check_mouse_position()
        px.text(140, 70, f'The Doom caught you. You Lost!', 7)
        px.text(140, 80, f'Click to play again', 7)


    def check_mouse_position(self):
        if px.btnr(px.MOUSE_BUTTON_LEFT):
            self._next_state = TitleScreen(self.game)