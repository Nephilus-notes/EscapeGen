import pyxel as px 
from src.utils import Interactable, Layer, Runners


class DisplayText:
    def __init__(self,x, y, stat_name, col=7, owner=None) -> None:
        self.x = x
        self.y = y
        self.stat_name = stat_name
        self.col = col

    def draw(self):
        px.text(self.x, self.y, f'{self.stat_name}:{self.owner} ', self.col)


class DisplayImage:
    """Parent class for all displayed objects"""
    def __init__(self, x, y, bank, u, v, w, h, colkey=7) -> None:
        self.x = x
        self.y = y
        self.bank = bank
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey

    def draw(self):
        px.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, colkey= self.colkey)

# class DisplayTopLayer(DisplayImage):
#     def __init__(self, x, y, bank, u, v, w, h, colkey=7) -> None:
#         super().__init__(x, y, bank, u, v, w, h, colkey)

class Sprite(DisplayImage): 
    """Parent class for all objects that can move"""
    def __init__(self, u, v, x=96, y=24, bank=2, w=16, h=16, colkey=7) -> None:
        super().__init__(x, y, bank, u, v, w, h, colkey)
        self.running= False

    def run(self):
        if self.running == False:
            self.y -= 2
            # // Transforming logic //
            # self.u += 8
            self.running = True
        elif self.running == True:
            self.y += 2
            # // Transforming logic //
            # self.u -= 8
            self.running = False
    
    def start_running(self):
        Runners.main.append(self)

    
    def combat_draw(self):
        px.text(73, 1, f"{self.name}", 7)


class Background(DisplayImage):
    """Class for all background images"""
    def __init__(self,  u, v, bank=0, x=72, y=8, w=128, h=128):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.u = u
        self.v = v
        self.bank = bank

        super().__init__(self.x, self.y, self.bank, self.u, self.v, self.w, self.h)

    def draw(self):
        px.bltm(self.x, self.y, tm=self.bank, u=self.u, v=self.v, w=self.w, h=self.h)


class Tile(Background):
    """Class for all tiles"""
    def __init__(self, u, v, bank, x, y, w=16, h=16):
        self.sight_modifier = .5
        self.name = ''
        super().__init__(u, v, bank, x, y, w, h)

        if self.u == 0 and self.v == 0:
            self.colkey = 0
            self.name = "Forest"
            self.speed_modifier = .8
            self.sight_modifier = .8

        if self.u == 16 and self.v == 0:
            self.colkey = 1
            self.name = "Mountain"
            self.speed_modifier = .2
            self.sight_modifier = .2

        if self.u == 32 and self.v == 0:
            self.colkey = 0
            self.name = "Grassland"
            self.speed_modifier = 1
            self.sight_modifier = 1

        if self.u == 48 and self.v == 0:
            self.colkey = 0
            self.name = "Desert"
            self.speed_modifier = 1.1
            self.sight_modifier = 1.1

        if self.u == 16 and self.v == 16:
            self.colkey = 0
            self.name = "Water"
            self.speed_modifier = .5
            self.sight_modifier = 1.4

        if self.u == 0 and self.v == 16:
            self.colkey = 7
            self.name = "Cave"
            self.speed_modifier = 1
            self.sight_modifier = 1

    def draw(self):
        px.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, colkey=7)

    def intersects(self, character_location:tuple):
        is_intersected = False
        if (
            character_location[0] > self.x and character_location[1] < self.x + self.w
            and character_location[1] > self.y and character_location[1] < self.y + self.h + 2
        ):
            is_intersected = True
            return is_intersected
        
    def sight_intersect(self, sight_lines:list):
        is_intersected = False
        if (self.x in range(sight_lines[0][0], sight_lines[0][1]) and self.y in range(sight_lines[1][0], sight_lines[1][1])
            or self.x + self.w in range(sight_lines[0][0], sight_lines[0][1]) and self.y in range(sight_lines[1][0], sight_lines[1][1])
            or self.x in range(sight_lines[0][0], sight_lines[0][1]) and self.y + self.h in range(sight_lines[1][0], sight_lines[1][1])
            or self.x + self.w in range(sight_lines[0][0], sight_lines[0][1]) and self.y + self.h in range(sight_lines[1][0], sight_lines[1][1])):
                is_intersected = True
                return is_intersected
    
    def sight_intersection(self):
        return self.sight_modifier

    def intersection(self) -> float:
        return self.speed_modifier
        

    def draw(self):
        px.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, colkey=7)

    def intersects(self, character_location:tuple):
        is_intersected = False
        if (
            character_location[0] > self.x and character_location[1] < self.x + self.w
            and character_location[1] > self.y and character_location[1] < self.y + self.h + 2
        ):
            is_intersected = True
            return is_intersected

    def intersection(self) -> float:
        return self.speed_modifier


class Clickable:
    """"parent class for all objects that use hover or on click effects"""
    def intersects(self, mouse_location:tuple):
        is_intersected = False
        if (
            px.mouse_x > self.x and px.mouse_x < self.x + self.w
            and px.mouse_y > self.y and px.mouse_y < self.y + self.h + 2
        ):
            is_intersected = True
            return is_intersected

    def intersection(self):
        pass

    def interact(self):
        Interactable.main.append(self)
        if self in Interactable.frozen:
            Interactable.frozen.remove(self)

    def freeze(self):
        Interactable.main.remove(self)
        Interactable.frozen.append(self)

    def unfreeze(self):
        Interactable.frozen.remove(self)
        Interactable.main.append(self)

class Entrance(DisplayImage, Clickable):
    """ Images that display and use hover/onflick to provide routing from the townscreen"""
    def __init__(self, game_state:object, entrance_dict:dict):
        self.name= entrance_dict['name']
        self.x = entrance_dict['x']
        self.y = entrance_dict['y']
        self.bank = entrance_dict['bank']
        self.u = entrance_dict['u']
        self.v = entrance_dict['v']
        self.w = entrance_dict['w']
        self.h = entrance_dict['h']
        self.colkey = entrance_dict['colkey']
        self.entrance_dict = entrance_dict
        self.color = entrance_dict['color']
        self.offset = entrance_dict['offset']
        self.owner = game_state
    
    def intersection(self):
        self.flag = Pointer(self.entrance_dict)
        self.flag.draw()
        px.text(self.x - self.offset, self.y - 24, self.name, self.color)


# class ShopItem(Clickable, DisplayImage):
#     """Items to display in the shop that will (eventually) hook up to the items dictionary"""
#     def __init__(self, player:object, x, y, u, v, w, h, name, item_stat, price, slot, id, description, bank=2, colkey=7) -> None:
#         super().__init__(x, y, bank, u, v, w, h, colkey)
#         self.item_stat = item_stat
#         self.price = price
#         self.name =name
#         self.slot = slot
#         self.description =description
#         self.id = id
#         self.player = player
#         self.on_creation()

#     def intersection(self):
#             self.item_text()
#             if px.btn(px.MOUSE_BUTTON_LEFT):
#                 if self.player.currency < self.price:
#                     return px.text(81, 56, "More Trophies", 7)
                    
#                 self.freeze()
#                 self.player.currency -= self.price
                
#                 Layer.main.remove(self)
                
#                 if self.id in range(0, 8):

#                     self.player.bag.add_item(PlayerEquippableItem(self.player,
#                         self.x, self.y, self.u, self.v, self.w, self.h, 
#                         self.name, self.item_stat, self.price, self.slot, 
#                         self.id, self.description
#                     ))

#                 elif self.id in range(8, 11):

#                     x = 208

#                     new_potion = PlayerConsumableItem(self.player,
#                         x, self.y, self.u, self.v, self.w, self.h, 
#                         self.name, self.item_stat, self.price, self.slot, 
#                         self.id, self.description
#                     )

#                     self.player.bag.add_potion(new_potion)

#     def item_text(self):
#             px.text(84, 84, self.name, 7)
#             px.text(84, 96, f"Price: {self.price} ", 7)
#             px.text(127, 96, f'Slot: {self.slot}', 7)
#             px.text(83, 103, f'{self.description}', 7)
#             if self.id in range(3) or self.id == 7:
#                 px.text(84, 103, f'DAM: {self.item_stat}', 7)
#             elif self.id in range(3, 6):
#                 px.text(84, 103, f"DEF: {self.item_stat}", 7)
#             elif self.id in range(8,11):
#                 px.text(84, 103, f'HEAL: {self.item_stat}', 7)
            
#     def on_creation(self):
#         pass
#                 # add a conditional to instantiation to check if something with 
#                 # the same id exists in the player inventory
    


# class PlayerEquippableItem(ShopItem):
#     def on_creation(self):
#         self.start_drawing()
#         self.bag_id = 0

#     def start_drawing(self):
#         Layer.main.append(self)

#     def intersection(self):
#         px.blt(76, 84, 1, 0, 192, 120, 48)
#         self.item_text()

#         if self.player.game_state.is_clicking():
#             if self.y == 88 or self.y == 112:
#                 self.player.bag.add_item(self)
#                 self.player.bag.equipped.slot[self.slot] = {'nothing':'nothing'}
#                 return


#             self.player.bag.equip(self)
#             self.is_interacting = True






# class PlayerConsumableItem(ShopItem):
#     def on_creation(self):
#         self.quantity = 0
#         if self.quantity> 1:
#             self.start_drawing()

#     def start_drawing(self):
#         Layer.main.append(self)

#     def intersection(self):
#         px.blt(76, 84, 1, 0, 192, 120, 48)
#         self.item_text()
#         if px.btnr(px.MOUSE_BUTTON_LEFT):
#             if self.player.current_hp == self.player.hp:
#                 pass
#             else:
#                 try:
#                     self.freeze()
                    
#                     self.player.bag.use_potion(self)
#                 except:
#                     print('tried to drink potion')



class Button(Clickable, DisplayImage): 
    def __init__(self, owner=None, x=152, y=127, bank=1, u=0, v=0, w=32, h=8, colkey=10, use:str = "Town") -> None:
        super().__init__(x, y, bank, u, v, w, h, colkey)
        self.owner = owner
        self.use= use

    def draw(self):
        px.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, colkey= self.colkey)
        px.text(self.x + 8, self.y +2, F'{self.use}', 7)

class StartGameButton(Button):
    def __init__(self, owner=None, x=120, y=88, bank=0, u=40, v=144, w=64, h=16, colkey=10, use: str = "Start Game") -> None:
        super().__init__(owner, x, y, bank, u, v, w, h, colkey, use)

class ExploreButton(Button):
    def __init__(self, owner, x=88, y=127, bank=1, u=0, v=0, w=32, h=8, colkey=10) -> None:
        super().__init__(owner, x, y, bank, u, v, w, h, colkey)
    
    def draw(self):
        px.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, colkey= self.colkey)
        px.text(self.x + 2, self.y +2, "Explore", 7)

class Pointer(Sprite):
    """A companion for the houses on the town screen to give info on what the house is."""
    def __init__(self, entrance_dict:dict) -> None:
        self.x = entrance_dict['x']
        self.y = entrance_dict['y'] - 16
        self.u = entrance_dict['u']
        self.bank = entrance_dict['bank']
        self.v = entrance_dict['v']-16
        self.w = entrance_dict['w']
        self.h = entrance_dict['h']
        self.colkey = 0
        super().__init__(x=self.x, y=self.y, bank=self.bank, u=self.u, v= self.v, w=self.w, h=self.h, colkey=self.colkey)

