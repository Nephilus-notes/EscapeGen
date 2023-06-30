from src.image_classes import Sprite 
import pyxel as px

class Player(Sprite):

    def __init__(self, u, v, fog_layer = [], x=72, y=8, bank=0, w=8, h=8, colkey=7) -> None:
        super().__init__(u, v, x, y, bank, w, h, colkey)
        self.direction = "Down"
        self.speed = 8
        self.adjusted_speed = self.speed

        self.fog_layer = fog_layer

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

        self.check_sight()


    def check_sight(self,):
        """Checks the sight of the player in a given direction."""

        """Adjust sight to make it longer.  Up to 24 in the direction you are facing and 16 in other directions. Might require fog tiles to be only 8 in size"""
        if self.direction == "Up":
            # if tiles in the fog layer exist in the player's x and y values or the player's y value - 16 remove the tile from the fog layer

            for tile in self.fog_layer:
                if tile.y >= self.y - 16 and tile.y <= self.y and tile.x >= self.x - 8 and tile.x <= self.x:
                    self.fog_layer.remove(tile)

        elif self.direction == "Down":
            for tile in self.fog_layer:
                if tile.y <= self.y + 8 and tile.y >= self.y and tile.x >= self.x - 8 and tile.x <= self.x:
                    self.fog_layer.remove(tile)


        elif self.direction == "Left":
            for tile in self.fog_layer:
                if tile.x <= self.x and tile.x >= self.x - 16 and tile.y >= self.y -8 and tile.y <= self.y:
                    self.fog_layer.remove(tile)

        elif self.direction == "Right":
            for tile in self.fog_layer:
                if tile.x <= self.x + 8 and tile.x >= self.x and tile.y >= self.y -8 and tile.y <= self.y:
                    self.fog_layer.remove(tile)