import pyxel
from collections import deque

class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.skin_dict = {    'RIGHT_1' :[0,0,0,8,8],
                           'LEFT_1' :[0,8,0,8,8],
                          'RIGHT_2' :[0,0,8,8,8],
                           'LEFT_2' :[0,8,8,8,8],
                           'DOWN_1' :[0,0,32,8,8],
                           'DOWN_2' :[0,8,32,8,8],
                           'UP_1' :[0,0,24,8,8],
                           'UP_2' :[0,8,24,8,8],
                           'ATTACK_L_1': [0,16,0,16,8],
                           'ATTACK_L_2': [0,16,8,16,8],
                           'ATTACK_L_3': [0,16,16,16,8],
                           
                           }
        self.skin = 'RIGHT_1'
        self.att = False
        self.sword = Sword()
    
    def draw(self):
        pyxel.blt(self.x, self.y, *self.skin_dict[self.skin],000000)
        self.sword.draw()
     
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.move_animation('LEFT_1')
            self.x = max(self.x - 2, 0)
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.move_animation('RIGHT_1')
            self.x = min(self.x + 2, pyxel.width - 16)
            
        if pyxel.btn(pyxel.KEY_DOWN):
            self.move_animation('DOWN_1')
            self.y = max(self.y + 2, 0)
            
        if pyxel.btn(pyxel.KEY_UP):
            self.move_animation('UP_1')
            self.y = min(self.y - 2, pyxel.width - 16)
        
        # if pyxel.btn(pyxel.KEY_SPACE):
        #     self.attack()
        
        self.sword.update()

    def attack(self):
        self.att = True
        for i in range(3):
            print('attack() == ')
            self.sword.update()
                # time.sleep(.3)
            
        
        
    def move_animation(self, start_skin):
        if "1" not in self.skin:
            self.skin = start_skin[:-2] + "_1"
        else: self.skin = start_skin[:-2] + "_2"
    
    
    
class Sword:
    
    def __init__(self):
        self.x = 20
        self.y = 20
        self.skin = 'L_3'
        self.direction = "LEFT"
        self.active = False
        self.frame = 0 
        self.animation_frame = 0
        self.height = 8
        self.width = 8
        
    def draw(self):
        print(self.animation_frame)
        # if cls.active:
        pyxel.blt(self.x, self.y, img=0, u=16,v=self.height*self.animation_frame, w=self.width,h=self.height,colkey=000000)
    
    def update(self):
        print('sword_update')
        
        # if cls.active == False:
            # print(skin, ' -- skin before')
            # cls.sword.direction = skin
            # start_skin - ''
            # if cls.direction == "L":
                # self.skin = 'L_1'
        #         cls.x +=-8
        #         cls.active = True
        #         cls.skin = 'L_1'
        #         # self.attack('L_1')
                
        #     elif cls.direction == "R":
        #         cls.x +=8
        #         cls.active = True
        #         cls.skin = 'R_1'
        #     else: 
        #         cls.skin = 'NONE'
        #     print(cls.direction, ' -- self direction')
        # # for i in self.attack():
        # #    self.skin = i
        
        self.animation_frame = self.frame // 3 % 3
        self.frame += 1
        
class App:
    def __init__(self):
        pyxel.init(160, 120,fps=8)
        pyxel.load("my_resource.pyxres")
        self.hero = Hero()
        pyxel.run(self.update, self.draw)
        
        self.setup()

    def setup(self):
        pass
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.hero.update()

    def draw(self):
        pyxel.cls(0)
        self.hero.draw()

App()