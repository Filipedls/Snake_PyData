import random
import pygame as pg
from .files import regr
from .features import compute_all_feats
from .config import SCR_SZ, get_apple_location_from_model


class snake():
    def __init__(self,speed, size):
        self.star_snk_size = 1#random.randrange(1, 14,1)
        self.added_starting_apples = 0
        self.pos = [random.randrange(90, SCR_SZ[0]-80,30), random.randrange(90, SCR_SZ[1]-80,30)]
        self.image = pg.Surface((10*size,10*size))
        self.image.fill((0,255,0))
        self.speed = speed
        self.size = size
        self.images = []
        self.old_pos = [self.pos.copy()]
        self.direction = [0,0]
        self.score = 0#self.star_snk_size-1
    def right(self):
        self.direction = [self.speed,0]
    def left(self):
        self.direction = [-self.speed,0]
    def up(self):
        self.direction = [0,-self.speed]
    def down(self):
        self.direction = [0, self.speed]
    def adding_starting_apples(self):
        return self.added_starting_apples < self.star_snk_size-1
    def get_snake_position(self):
        pos = [self.pos.copy()] + [x[1].copy() for x in self.images]
        return pos
    def update(self):
        if self.old_pos[-1] != self.pos:
            self.old_pos.append([self.pos[0],self.pos[1]])
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        a = 1

        if self.adding_starting_apples() and \
            (len(self.old_pos) >= int((self.added_starting_apples+1)*((11*self.size)/self.speed))):
            self.add_blocks()
            self.added_starting_apples += 1

        for x in self.images:
            neg_idx = int(a*((-11*self.size)/self.speed))
            if len(self.old_pos) >= -neg_idx:
                x[1] = self.old_pos[neg_idx]
            a += 1

    def check_collisions(self, x):
        c=collide(self.pos[0], self.pos[1],self.pos[0]+10,self.pos[1]+10,x[0],x[1],x[0]+3,x[1]+3)
        return c
    def check_apple(self,x):
        c=collide2(self.pos[0],self.pos[1],self.pos[0]+10,self.pos[1]+10,x[0],x[1],x[0]+10,x[1]+10, self.size)
        return c
    def check_collisions2(self,x):
        c=collide3(self.pos[0],self.pos[1],self.pos[0]+10,self.pos[1]+10,x[0],x[1],x[0]+10,x[1]+10, self.size)
        return c
    def add_apple(self):
        #self.score +=1
        # When there are still starting apples to add shouldn't add a block
        if self.adding_starting_apples():
            self.added_starting_apples -= 1
        else:
            self.add_blocks()

    def add_blocks(self, n_blocks=1):
        self.score +=1
        block = pg.Surface((10*self.size,10*self.size))
        block.fill((0,255,0))
        self.images.extend(n_blocks*[[block, self.images[-1][1].copy() if len(self.images)!=0 else [10,10]]]) #[10,10]]])


class apple():
    def __init__(self,size, snake_pos, snake_dir, game_score):

        self.set_new_apple_position(snake_pos, snake_dir, game_score)

        self.image = pg.Surface((10*size,10*size))
        self.image.fill((255,0,0))

    def set_new_apple_position(self, snake_pos, snake_dir, game_score):
        if get_apple_location_from_model:
            # Compute features and predicts
            feats = compute_all_feats(snake_pos, snake_dir, game_score)
            self.pos = list(regr.predict(feats.reshape(1, -1)).reshape(-1))
            self.check_position()
        else:
            self.pos = [random.randrange(10, SCR_SZ[0]-20,10),random.randrange(10,SCR_SZ[1]-20,10)]

    def check_position(self, x_lim=[10, SCR_SZ[0]-20], y_lim=[10,SCR_SZ[1]-20]):
        """
        Clips the prediction to not leave the screen size
        """
        # X
        if self.pos[0] < x_lim[0]:
            self.pos[0] = x_lim[0]
        elif self.pos[0] > x_lim[1]:
            self.pos[0] = x_lim[1]
        # Y
        if self.pos[1] < y_lim[0]:
            self.pos[1] = y_lim[0]
        elif self.pos[1] > y_lim[1]:
            self.pos[1] = y_lim[1]


# The functions that check for collisions
def collide(x1,y1,x2,y2,x3,y3,x4,y4):
    if (x3+x4) > x1 > x3 and (y3+y4) > y1 > y3 or (x3+x4) > x2 >x3 and (y3+y4) > y2 > y3:
        return True
    else:
        return False


def collide2(x1,y1,x2,y2,x3,y3,x4,y4,size):
    n=7
    if (x3+(n*size)) > x1 > x3-(n*size) and (y3+(n*size)) > y1 > y3-(n*size) or (x3+(n*size)) > x2 >x3-(n*size) and (y3+(n*size)) > y2 > y3-(n*size):
        return True
    else:
        return False


def collide3(x1,y1,x2,y2,x3,y3,x4,y4,size):
    if (x3+(5*size)) > x1 > x3 and (y3+(5*size)) > y1 > y3 or (x3+(5*size)) > x2 >x3 and (y3+(5*size)) > y2 > y3:
        return True
    else:
        return False
