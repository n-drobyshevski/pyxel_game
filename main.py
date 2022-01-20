import pyxel
import math

WALL_TILE_X = 6
TRANSPARENT_COLOR = 0
SCROLL_BORDER_X_R = 80
SCROLL_BORDER_X_L = 54
JUMP_HEIGHT = 12
TILE_SPAWN1 = (4, 2)
MAP_MAX_X =  240 * 8
SPIKE_X = [2,3] 
SPIKE_Y = [5,6] 

scroll_x = 0
enemies =[] 
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

def is_spike(x,y):
    x = x // 8
    y = y // 8
    tile = pyxel.tilemap(0).pget(x,y)
    if tile[0] in SPIKE_X and tile[1] in SPIKE_Y:
        return True
    return False


# TODO: replace with get_tile()

def is_wall(x,y):
    x = x // 8
    y = y // 8
    tile = pyxel.tilemap(0).pget(x,y)
    if tile[0] >= WALL_TILE_X:
        return True
    return False

def spawn_enemy():
    left_x = math.ceil(0 / 8)
    right_x = math.floor(320 / 8)
    for x in range(left_x, right_x + 1):
        for y in range(16):
            tile = get_tile(x, y)
            if tile == TILE_SPAWN1:
                enemies.append(Enemy(x * 8, y * 8))

def is_pit(x,y,direction):
    if not (y +16 < 128 and x -8 > 0 and x +16 < MAP_MAX_X):
        return False

    if direction > 0:
        if is_wall(x+8,y+4):
            return False
    else: 
        if is_wall(x-1,y+4):
            return False

    y1 = y +12
    if direction > 0:
        if is_wall(x+8,y1):
            return False
    else:
        if is_wall(x-1,y1):
            return False

    y2 = y +16
    if direction > 0:
        if is_wall(x+4,y2):
            return False
    else:
        if is_wall(x-1,y2):
            return False
    return True

def can_jump(x,y,direction):
    if not (y +16 < 128 and x -8 > 0 and x +16 < MAP_MAX_X):
        return False

    if direction > 0:
        if not is_wall(x+8,y+4):
            return False
    else: 
        if not is_wall(x-1,y+4):
            return False
    y1 = y -12
    if direction > 0:
        if is_wall(x+8,y1):
            return False
    else:
        if is_wall(x-1,y1):
            return False
    
    return True

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.is_alive:
            i += 1
        else:
            list.pop(i)
class Player:
    def __init__(self,x,y):
        self.direction = -1
        self.frame = 0 
        self.height = 8
        self.jump_height = 10
        self.sword = Sword()
        self.d_y = 0
        self.d_x = 0
        self.x = x
        self.y =y
        self.start_y = 0
        self.falling = False
        self.is_alive = True
        
    def draw(self):
        v = (1 if self.falling else self.frame// 3 % 2) * 8 +8 
        w = 8 if self.direction < 0 else -8
        # TODO: weird +8 
        pyxel.blt(self.x, self.y, img=0, u=0,v=v, w=w,h=self.height,colkey=TRANSPARENT_COLOR)
        self.sword.draw()
     
    def update(self):
        global scroll_x
        wall_x = [0,0]
        last_y = self.y
        if is_spike(self.x, self.y):
            self.is_alive = False
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = 1
            self.d_x = -2
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = -1
            self.d_x = 2
            self.frame += 1
        
        self.d_y = min(self.d_y + 1, 3)
        if pyxel.btn(pyxel.KEY_SPACE) and self.start_y - JUMP_HEIGHT< self.y and self.falling == False:   
            self.d_y = -6   #if space pressed begins to add -1 to self.y

        self.x, self.y, self.d_x, self.d_y, collision_side = move(self.x, self.y, self.d_x, self.d_y)
        if self.y > last_y or collision_side[1] == -1:
            self.falling = True
        
        if collision_side[1] == 1:
            self.start_y = self.y
            self.falling = False

        if pyxel.btn(pyxel.KEY_Q):
            wall_x[0] = detect_collision(self.x+8, self.y)
            wall_x[1] = detect_collision(self.x-8, self.y)
            if self.sword.active == False:
                self.sword.set_visible(wall_x)
    
        if self.x < 0:
            self.x = 0
        if self.x > 248*8:
            self.x = 248*8
        if self.y > 128-self.height:
            self.y = 128-self.height
        
        if self.x > scroll_x + SCROLL_BORDER_X_R:
            scroll_x = min(self.x - SCROLL_BORDER_X_R, MAP_MAX_X)

        elif self.x < scroll_x + SCROLL_BORDER_X_L and scroll_x >= 0:
            scroll_x = max(self.x - SCROLL_BORDER_X_L, 0)

        self.sword.update(self.x, self.y, self.direction)
    
class Sword:
    
    def __init__(self):
        self.x = 20
        self.y = 20
        self.active = False
        self.frame = 0 
        self.animation_frame = 0
        self.width = 8
        self.u=0
        self.direction = 1
        
        
    def draw(self):
        v = self.animation_frame*8
        w = 8 if self.direction > 0 else -8
        if self.active:
            pyxel.blt(self.x, self.y, img=0, u=16,v=v, w=w,h=8,colkey=TRANSPARENT_COLOR)
    
    
    def update(self,x,y,direction):
        self.y = y
        self.direction = direction
        if direction == 1:  
            self.x = x-8
        elif direction == -1:
            self.x = x + 8
            
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1
        if self.animation_frame == 3:
            self.set_invisible()
            
        
    def set_visible(self,wall):
        index = (1 if self.direction == 1 else 0)
        if wall[index] == False:
            self.active = True
            self.frame=0
        
    def set_invisible(self):
        self.active = False
    
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d_x = 0
        self.d_y = 0
        self.direction = -1
        self.is_alive = True
        self.frame = 0

    def update(self):
        self.d_x = self.direction
        self.d_y = min(self.d_y + 1, 3)
        if is_pit(self.x, self.y, self.direction):
            self.direction = self.direction* -1
        if self.direction < 0 and is_wall(self.x - 1, self.y + 4) and can_jump(self.x,self.y,self.direction) == False:
            self.direction = 1
        elif self.direction < 0 and can_jump(self.x,self.y,self.direction):
            print("jump")
            self.d_y = -3
            self.d_x = -4
        elif self.direction > 0 and is_wall(self.x + 8, self.y + 4 and can_jump(self.x,self.y,self.direction)== False):
            self.direction = -1
        elif self.direction < 0 and can_jump(self.x,self.y,self.direction):
            print("jump")
            self.d_y = -3
            self.d_x = 12

        if self.x < 0:
            self.x = 0 
            self.direction = 1
        self.frame += 1
        self.x, self.y, self.d_x, self.d_y, collision_side = move(self.x, self.y, self.d_x, self.d_y)

    def draw(self):
        v = self.frame % 2 * 8 +8
        w = -6 if self.direction < 0 else 6 
        pyxel.blt(self.x, self.y, img=0, u=50,v=v, w=w,h=8,colkey=TRANSPARENT_COLOR)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Pyxel Platformer", fps = 40)
        pyxel.load("my_resource.pyxres")
        global player
        player = Player(0,0)
        spawn_enemy()
        pyxel.run(self.update, self.draw)
        self.setup()

    def setup(self):
        pass
        
    def update(self):
        pyxel.mouse(visible=True)
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if player.is_alive == False:
            reset()
            return
        player.update()
        for enemy in enemies:
            enemy.update()
        cleanup_list(enemies)

    def draw(self):
        pyxel.cls(0)
        pyxel.camera()
        pyxel.bltm(0, 0, 0, scroll_x, 0, 128, 128,TRANSPARENT_COLOR)
        
        # Draw characters
        pyxel.camera(scroll_x, 0)
        player.draw()
        for enemy in enemies:
            enemy.draw()

def reset():
    global scroll_x, enemies
    scroll_x = 0
    player.x = 0
    player.y = 0
    player.d_x = 0
    player.d_y = 0
    player.is_alive = True
    enemies = []
    spawn_enemy()

App()