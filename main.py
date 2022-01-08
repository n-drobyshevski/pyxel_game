import pyxel
import time

class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.skin_dict = {    'RIGHT' :[0,0,0,8,8],
                               'LEFT' :[0,8,0,8,8],
                          'RIGHT_1' :[0,0,8,8,8],
                           'LEFT_1' :[0,8,8,8,8],
                           'DOWN' :[0,0,32,8,8],
                           'DOWN_1' :[0,8,32,8,8],
                           'UP' :[0,0,24,8,8],
                           'UP_1' :[0,8,24,8,8],}
        self.skin = 'RIGHT'
    
    def draw(self):
        pyxel.blt(self.x, self.y, *self.skin_dict[self.skin])
     
    def update(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_animation('LEFT')
            self.x = max(self.x - 2, 0)
            
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_animation('RIGHT')
            self.x = min(self.x + 2, pyxel.width - 16)
            
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.move_animation('DOWN')
            self.y = max(self.y + 2, 0)
            
        if pyxel.btnp(pyxel.KEY_UP):
            self.move_animation('UP')
            self.y = min(self.y - 2, pyxel.width - 16)

    def move_animation(self, start_skin):
        if "1" not in self.skin:
            self.skin = start_skin + "_1"
        else: self.skin = self.skin[:-2]

class App:
    def __init__(self):
        pyxel.init(160, 120,fps=8)
        pyxel.load("my_resource.pyxres")
        self.hero = Hero()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.hero.update()

    def draw(self):
        pyxel.cls(0)
        self.hero.draw()

App()