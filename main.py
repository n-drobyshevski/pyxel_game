from operator import invert
import pyxel
from collections import deque

class Hero:
    def __init__(self):
        self.x = 20
        self.y = 50
        self.active = False
        self.frame = 0 
        self.animation_frame = 0
        self.height = 8
        self.width = 8
        self.u=0
        self.jump_height = 10
        self.sword = Sword()
        self.jump = False
        self.fall = False
        self.d_y = 0
        
        
    def draw(self):
        pyxel.blt(self.x, self.y, img=0, u=self.u,v=self.height*self.animation_frame, w=self.width,h=self.height,colkey=000000)
        self.sword.draw()
     
    def update(self):
        top = False
        fall = False
        if pyxel.btn(pyxel.KEY_LEFT):
            self.u = 8
            self.x = max(self.x - 1, 0)
            
            self.animation_frame = self.frame // 3 % 2
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.u = 0
            self.x = min(self.x + 1, pyxel.width - 16)
            self.animation_frame = self.frame // 3 % 2
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_SPACE) and self.jump == False:       
            if self.jump== False:
                print(1)
                self.jump = True
                self.d_y = -1
                
        if self.y == 29: 
            self.fall = True 

        if self.fall == True and self.y < 70:
            print(2)
            self.d_y = 1

        elif self.y == 71: 
            self.d_y = 0
            self.y -=1
            self.fall = False
            self.jump = False

        if pyxel.btn(pyxel.KEY_Q):
            self.sword.set_visible()
        print(self.y, self.jump, self.d_y)
        self.y += self.d_y
    
        self.sword.update(self.x, self.y,self.u)
    
    
class Sword:
    
    def __init__(self):
        self.x = 20
        self.y = 20
        self.active = False
        self.frame = 0 
        self.animation_frame = 0
        self.height = 8
        self.width = 8
        self.u=0
        
        
    def draw(self):
        if self.active:
            pyxel.blt(self.x, self.y, img=0, u=self.u,v=self.height*self.animation_frame, w=self.width,h=self.height,colkey=000000)
    
    
    def update(self,x,y,direction):
        self.y = y
        if direction == 8:
            self.u = 16
            self.x = x-8
        elif direction == 0:
            self.x = x + 8
            self.u = 24
        else: 
            self.u = 50
            
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1
        if self.animation_frame == 3:
            self.set_invisible()
            
        
    def set_visible(self):
        self.active = True
        self.frame=0
        
    def set_invisible(self):
        self.active = False
class App:
    def __init__(self):
        pyxel.init(160, 120,fps=30)
        pyxel.load("my_resource.pyxres")
        self.hero = Hero()
        pyxel.run(self.update, self.draw)
        
        self.setup()

    def setup(self):
        pass
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            
        self.hero.update()

    def draw(self):
        pyxel.cls(0)
        self.hero.draw()
        pyxel.blt(60,60,1,0,0,4,4)
        pyxel.blt(60,40,1,0,0,8,8)
        pyxel.blt(60,20,1,0,0,16,16)
App()