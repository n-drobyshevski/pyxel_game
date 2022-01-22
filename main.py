import pyxel
import math
import time 

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
    # check if there is wall ahead
    y0 = y+4
    if direction > 0:
        if is_wall(x+8,y0):
            return False
    else: 
        if is_wall(x-1,y0):
            return False
    # check if there is wall one block ahead and one block down
    y1 = y +8
    if direction > 0:
        if is_wall(x+8,y1):
            return False
    else:
        if is_wall(x-1,y1):
            return False

    # return false if there is map border one block ahead and two block down
    if not (y +16 < 128 and x -8 > 0 and x +16 < MAP_MAX_X):
        return True
    # check if there is wall one block ahead and two block down
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
        self.can_reset = False

    def draw(self):
        if self.is_alive:
            v = (1 if self.falling else self.frame// 3 % 2) * 8 +8 
        else: 
            v = 24
        w = 8 if self.direction > 0 else -8
        # TODO: weird +8 
        pyxel.blt(self.x, self.y, img=0, u=0,v=v, w=w,h=self.height,colkey=TRANSPARENT_COLOR)
        self.sword.draw()
     
    def update(self):
        global scroll_x,enemies
        wall_x = [0,0]
        last_y = self.y
        if is_spike(self.x, self.y):
            self.is_alive = False
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = -1
            self.d_x = -2
            self.frame += 1
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = 1
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

        self.sword.update(self.x, self.y, self.direction,0)
        if self.is_alive == False:
            for enemy in enemies:
                print(enemy)
            self.y += 4
            time.sleep(2)
            self.can_reset = True
    
    def get_coords(self):
        list = []
        for x in range(self.x, self.x + 8):
            for y in range (self.y, self.y+8):
                list.append([x,y])
        return list
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
        self.skin = 0
        self.counter = 0
        
    def draw(self): 
        u = (16 if self.skin == 0 else 24)
        v = self.animation_frame*8
        w = 8 if self.direction<0 else -8
        if self.active:
            pyxel.blt(self.x, self.y, img=0, u=u,v=v, w=w,h=8,colkey=TRANSPARENT_COLOR)
    
    
    def update(self,x,y,direction, skin):
        self.skin = skin
        self.y = y
        self.direction = direction
        if direction == -1:  
            self.x = x-8
        elif direction == 1:
            self.x = x + 8
            
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1
        if self.active and self.detect_player():    
            player.is_alive = False
        if self.active and self.detect_enemy():    
            enemy = self.detect_enemy()
            enemy.is_alive = False
        if self.animation_frame == 3:
            self.counter +=1
            self.set_invisible()
            
        
    def set_visible(self,*args):
        if args:
            wall = args[0]
            index = (1 if self.direction == 1 else 0)
            if wall[index] == False:
                self.active = True
                self.frame=0
        else:
            self.active = True
            self.frame=0


    def set_invisible(self):
        self.active = False


    def detect_enemy(self):
        for enemy in enemies:
            enemy_coords = enemy.get_coords()
            if self.direction > 0:
                for [x, y] in enemy_coords:
                    if self.x+8  == x and self.y+4 == y:
                        return enemy
            if self.direction < 0:
                for [x, y] in enemy_coords:
                    if self.x-1  == x and self.y+4 == y:
                        return enemy
        return False


    def detect_player(self):
        player_coords = player.get_coords()
        if self.direction > 0:
            for [x, y] in player_coords:
                for xi in range(self.x, self.x +8):
                    if xi  == x and self.y+4 == y:
                        return True
        if self.direction < 0:
            for [x, y] in player_coords:
                for xi in range(self.x, self.x -9):
                    if xi  == x and self.y+4 == y:
                        return True
        return False
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d_x = 0
        self.d_y = 0
        self.direction = -1
        self.is_alive = True
        self.frame = 0
        self.sword = Sword()
    
    def __repr__(self) -> str:
        return f"""Enemy: 
                   at coords: x - {self.x}, y - {self.y}
                   turned to {('left' if self.direction < 0 else 'right')},
                   {('alive' if self.is_alive < 0 else 'dead')},
                   sword -- {('active' if self.sword.active< 0 else 'not active')}"""

    def update(self):
        self.d_x = self.direction
        self.d_y = min(self.d_y + 1, 3)
        if self.detect_player():
            self.d_x = 0
            self.attack()

        if is_pit(self.x, self.y, self.direction):
            self.direction = self.direction* -1
        if self.direction < 0 and is_wall(self.x - 1, self.y + 4) and can_jump(self.x,self.y,self.direction) == False:
            self.direction = 1
        elif self.direction < 0 and can_jump(self.x,self.y,self.direction):
            self.d_y = -3
            self.d_x = -4
        elif self.direction > 0 and is_wall(self.x + 8, self.y + 4 and can_jump(self.x,self.y,self.direction)== False):
            self.direction = -1
        elif self.direction < 0 and can_jump(self.x,self.y,self.direction):
            self.d_y = -3
            self.d_x = 12

        if self.x < 0:
            self.x = 0 
            self.direction = 1
        self.frame += 1
        self.x, self.y, self.d_x, self.d_y, collision_side = move(self.x, self.y, self.d_x, self.d_y)
        self.sword.update(self.x, self.y, self.direction, 1)

    def attack(self):
        if self.sword.active == False:
            self.sword.set_visible()


    def detect_player(self):
        player_coords = player.get_coords()
        if self.direction > 0:
            for [x, y] in player_coords:
                if self.x+8  == x and self.y+4 == y:
                    return True
        if self.direction < 0:
            for [x, y] in player_coords:
                if self.x-1  == x and self.y+4 == y:
                    return True
        return False

    def draw(self):
        v = self.frame % 2 * 8 +8
        w = -6 if self.direction < 0 else 6 
        pyxel.blt(self.x, self.y, img=0, u=10,v=v, w=w,h=8,colkey=TRANSPARENT_COLOR)
        self.sword.draw()

    
    def get_coords(self):
        list = []
        for x in range(self.x, self.x + 8):
            for y in range (self.y, self.y+8):
                list.append([x,y])
        return list
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
        if player.can_reset:
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
    player.can_reset = False
    enemies = []
    spawn_enemy()

App()