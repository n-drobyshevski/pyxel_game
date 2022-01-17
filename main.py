import pyxel


WALL_TILE_X = 4
MIN_X = 120
TRANSPARENT_COLOR = 14
JUMP_HEIGHT = 12

def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)

def detect_collision(x,y):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                return True
    return False


def move(x,y,d_x,d_y):
    abs_d_x = abs(d_x)
    abs_d_y = abs(d_y)
    collision_side = [0,0]
    if abs_d_x > abs_d_y:
        delta = 1 if d_x > 0 else -1
        for _ in range(abs_d_x):
            if detect_collision(x+delta, y):
                collision_side[0] = (1 if d_x > 0 else -1)
                break
            x += delta
        delta = 1 if d_y > 0 else -1
        print(delta, ' -- delta y')
        for _ in range(abs_d_y):
            if detect_collision(x, y+delta):
                collision_side[1] = (1 if d_y > 0 else -1)
                break
            y += delta
    else:
        delta = 1 if d_y > 0 else -1
        for _ in range(abs_d_y):
            if detect_collision(x, y + delta):
                collision_side[1] = (1 if d_y > 0 else -1)
                break
            y += delta
        delta = 1 if d_x > 0 else -1
        for _ in range(abs_d_x):
            if detect_collision(x + delta, y):
                collision_side[0] = (1 if d_x > 0 else -1)
                break
            x += delta
        d_x = 0
    return x,y,d_x,d_y, collision_side


class Hero:
    def __init__(self):
        self.active = False
        self.direction = -1
        self.frame = 0 
        self.animation_frame = 0
        self.height = 8
        self.jump_height = 10
        self.sword = Sword()
        self.jump_counter = 0
        self.d_y = 0
        self.d_x = 0
        self.x = 20
        self.y =MIN_X-self.height
        self.start_y = 0
        self.falling = False
        
    def draw(self):
        v = (1 if self.is_falling else self.frame// 3 % 2) * 8 +8
        w = -8 if self.direction > 0 else 8
        # todo: weird +8 
        pyxel.blt(self.x, self.y, img=0, u=0,v=v, w=w,h=self.height,colkey=TRANSPARENT_COLOR)
        self.sword.draw()
     
    def update(self):
        
        last_y = self.y
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = 1
            self.d_x = -1
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = -1
            self.d_x = 1
            self.frame += 1
        
        self.d_y = min(self.d_y + 1, 3)
        if pyxel.btn(pyxel.KEY_SPACE) and self.start_y - JUMP_HEIGHT<= self.y and not self.falling:   
            print(' key event ')   
            print(self.jump_counter)
            # self.start_y = self.y
            self.jump_counter +=1
            self.d_y = -2   #if space pressed begins to add -1 to self.y
        if self.start_y - JUMP_HEIGHT == self.y:
            self.falling = True

        # todo : add acceleration mechanic to delta y 
        # if max jump height achived   
        # todo : fix jump height

        self.x, self.y, self.d_x, self.d_y, collision_side = move(self.x, self.y, self.d_x, self.d_y)
        
        if collision_side[1] == 1:
            print(self.start_y,' ground ')
            self.start_y = self.y
            self.jump_counter = 0
            self.falling = False

        self.is_falling = self.y > last_y
        if pyxel.btn(pyxel.KEY_Q):
            # todo: fix multiply clicks
            self.sword.set_visible()

        
        if self.y < 0:
            self.y = 0
        if self.x < 0: 
            self.x = 0

        # print(self.y, self.jump, self.d_y)

        self.sword.update(self.x, self.y, self.direction)
    
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
        if direction == 1:
            self.u = 16
            self.x = x-8
        elif direction == -1:
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
        pyxel.init(128, 128, title="Pyxel Platformer", fps = 40)
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