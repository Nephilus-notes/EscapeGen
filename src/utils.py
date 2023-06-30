from time import time
from abc import ABC, abstractmethod
from threading import Timer

import pyxel as px

class Runners:
    main = []


class Updatable(ABC):

    updatables = []

    @abstractmethod
    def update(self, dt, t):
        pass

    def start_update(self):
        self.updatables.append(self)

    def stop_update(self):
        self.updatables.remove(self)


class Interactable:
    main = []
    frozen = []

    def freeze():
        Interactable.frozen += Interactable.main
        Interactable.main.clear()

    def unfreeze():
        Interactable.main += Interactable.frozen
        Interactable.frozen.clear()


class Layer:
    back = []  # background
    fog = []  # fog of war
    main = []  # Buildings, Characters
    fore = []  # Projectiles, on hit animations

class SpriteRunners:
    Runners = []

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

    def set_draw_layer(self, layer: Layer):
        if hasattr(self, "layer") and self in self.layer:
            self.stop_draw()
        self.layer = layer
        self.start_draw()

    def start_draw(self):
        self.layer.append(self)

    def stop_draw(self):
        self.layer.remove(self)


# Background location dict
background = {

    'title': {'u': 0, 'v': 0},
    'game_screen': {'u': 128, 'v': 0},
    'class_choice': {'u': 0, 'v': 512}
}


player_sprite_u_v = {
    "back": [0, 240],
    "front": [8, 240],
    "to_right": [16, 240],
    "to_left": [24, 240]
}

"""Tileset u and v values in order: Forest, Mountain, Grassland, Desert, Cave, Water"""
tile_list_u_v  =[
    [0, 0], [16, 0], [32, 0], [48, 0], [16, 16], [0, 16]
]

game_text = {}
