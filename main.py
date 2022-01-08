import pyxel

class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.skin_dict = {    'RIGHT' :[0,0,0,8,8],
                               'LEFT' :[0,8,0,8,8],
                          'RIGHT_RUN' :[0,0,8,8,8],
                           'LEFT_RUN' :[0,0,8,8,8]}
        self.skin = 'RIGHT'
    
    def draw(self):
        pyxel.blt(self.x, self.y, *self.skin_dict[self.skin])
                
    def run_animation(self,skin):
        if 'RUN' not in skin:
            if skin == 'RIGHT':
                self.skin = 'RIGHT_RUN'
            else:
                self.skin = 'LEFT_RUN'
        else:
            if skin == 'RIGHT_RUN':
                self.skin = 'RIGHT'
            else:
                self.skin = 'LEFT'
          
    def update(self):
        # while pyxel.btnp(pyxel.KEY_LEFT):
            
        #     self.run_animation('LEFT')
        #     self.x = max(self.x - 2, 0)
            
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
            self.skin = 'LEFT'
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 16)
            self.skin = 'RIGHT'
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = max(self.y + 2, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.y = min(self.y - 2, pyxel.width - 16)


class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("my_resource.pyxres")
        self.hero = Hero()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.hero.update()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
            self.hero.set_skin(self,'LEFT')
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
            self.hero.set_skin(self, 'RIGHT')
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = max(self.player_y + 2, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = min(self.player_y - 2, pyxel.width - 16)

    def draw(self):
        pyxel.cls(0)
        # pyxel.blt(x=0,y=0,img=0,u=8,v=0,h=8,w=8)
        self.hero.draw()

App()