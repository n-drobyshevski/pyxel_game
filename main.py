import pyxel


WALL_TILE_X = 4
MIN_X = 120
TRANSPARENT_COLOR = 14

def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)

def detect_collision(x,y):
    print(' --- entred in detect_collision')
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    print(x1,y1," || ",x2,y2, ' ---- x1 x2 y1 y2')
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            print(xi,yi, ' ---- ix, iy' )
            print(get_tile(xi, yi), '--- from get tile')
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                print(True)
                return True
    return False


def move(x,y,d_x,d_y):
    print(x,y,d_x,d_y, ' --- start')
    abs_d_x = abs(d_x)
    abs_d_y = abs(d_y)
    delta = 1 if d_x > 0 else -1
    print(delta, ' -- delta x')
    for _ in range(abs_d_x):
        print('entred in for')
        if detect_collision(x+delta, y):
            break
        x += delta
        print(x , ' -------------------- x')
    # delta = 1 if d_y > 0 else -1
    # print(delta, ' -- delta y')
    # for _ in range(abs_d_y):
    #     if detect_collision(x, y+delta):
    #         break
    #     y += delta
    print(x,y,d_x,d_y, ' --- end')
    print('------------------------------')
    print('------------------------------')
    return x,y,d_x,d_y


class Hero:
    def __init__(self):
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
        self.d_x = 0
        self.x = 20
        self.y =MIN_X-self.height
        self.start_y = MIN_X - self.height
        
    def draw(self):
        self.animation_frame = self.frame // 3 % 2
        pyxel.blt(self.x, self.y, img=0, u=self.u,v=self.height*self.animation_frame+8, w=self.width,h=self.height,colkey=TRANSPARENT_COLOR)
        self.sword.draw()
     
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.u = 8
            # self.x = max(self.x - 1, 0)
            self.d_x = -1
            # self.animation_frame = self.frame // 3 % 2
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.u = 0
            # self.x = min(self.x + 1, pyxel.width - 16)
            self.d_x = 1
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_SPACE) and self.jump == False:   
            print(' key event ')   
            self.start_y = self.y
            self.jump = True
            self.d_y = -1   #if space pressed begins to add -1 to self.y
        # todo : add acceleration mechanic to delta y 
        # if max jump height achived   
        # todo : fix jump height
        if self.y == self.start_y + 20: 
            self.fall = True 

        # falling
        if self.fall == True and self.y < MIN_X-self.height:
            self.d_y = 1

        # stop to falling
        elif self.fall == True and self.y == MIN_X-self.height: 
            self.d_y = 0
            # self.y -=1
            self.fall = False
            self.jump = False
        self.x, self.y, self.d_x, self.d_y = move(self.x, self.y, self.d_x, self.d_y)
        if pyxel.btn(pyxel.KEY_Q):
            self.sword.set_visible()
            ans = self.get_tile(20,20)
            ans2 = self.get_tile(20,127)
            ans3 = self.get_tile(self.x,self.y)
            print(ans)
            print(ans2)
            print(ans3, self.x, self.y)
            print('----')
        
        if pyxel.btn(pyxel.KEY_G):
           aa = pyxel.tilemap(0).pget(pyxel.mouse_x, pyxel.mouse_y)
           pyxel.tilemap(0).pset(pyxel.mouse_x,pyxel.mouse_y,(0,0))
           print( '--- ', aa , "  --- ")

        # print(self.y, self.jump, self.d_y)

        self.y += self.d_y
    
        self.sword.update(self.x, self.y,self.u)

    def get_tile(self,tile_x, tile_y):
        return pyxel.tilemap(0).pget(tile_x, tile_y)
    
        
    
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
            pyxel.blt(self.x, self.y, img=0, u=self.u,v=self.height*self.animation_frame, w=self.width,h=self.height,colkey=TRANSPARENT_COLOR)
    
    
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
        pyxel.init(128, 128, title="Pyxel Platformer")
        pyxel.load("my_resource.pyxres")
        self.hero = Hero()
        pyxel.run(self.update, self.draw)
        self.setup()

    def setup(self):
        pass
        
    def update(self):
        pyxel.mouse(visible=True)
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            
        self.hero.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.camera()
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128,TRANSPARENT_COLOR)
        self.hero.draw()
        
App()