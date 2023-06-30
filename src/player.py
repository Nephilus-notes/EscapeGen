from src.image_classes import Sprite 
import pyxel as px

class Player(Sprite):

    def __init__(self, u, v, x=72, y=8, bank=0, w=8, h=8, colkey=7) -> None:
        super().__init__(u, v, x, y, bank, w, h, colkey)
        self.direction = "Down"
        self.speed = 8

    def move(self):
        """Moves the player based on input, needs an additional condition
        to deal with nearing the edge of the screen."""
        if (px.btn(px.KEY_W) and self.direction != "Up"
        or px.btn(px.KEY_UP) and self.direction != "Up"):
            self.direction = "Up"
            self.u = 0
        elif px.btn(px.KEY_W) or px.btn(px.KEY_UP):
            self.y -= self.speed

        if (px.btn(px.KEY_S) and self.direction != "Down"
        or px.btn(px.KEY_DOWN) and self.direction != "Down"):
            self.direction = "Down"
            self.u = 8
        elif px.btn(px.KEY_S) or px.btn(px.KEY_DOWN):
            self.y += self.speed

        if (px.btn(px.KEY_A) and self.direction != "Left"
        or px.btn(px.KEY_LEFT) and self.direction != "Left"):
            self.direction = "Left"
            self.u = 24
        elif px.btn(px.KEY_A) or px.btn(px.KEY_LEFT):
            self.x -= self.speed

        if (px.btn(px.KEY_D) and self.direction != "Right"
        or px.btn(px.KEY_RIGHT) and self.direction != "Right"):
            self.direction = "Right"
            self.u = 16
        elif px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
            self.x += self.speed


    def update_sight():
        pass