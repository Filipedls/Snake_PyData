import pygame as pg
import sys
import time
from .files import file, close_file
from .game_objs import snake, apple
from .config import SCR_SZ

best_score = 0

class game():
    def __init__(self,speed, size=3, prev_game_score=None):
        self.screen = pg.display.set_mode((SCR_SZ[0],SCR_SZ[1]))
        self.snake = snake(speed, size)
        self.blocks = [] # wall blocks
        self.size = size
        self.left,self.right,self.up,self.down = False,False,False,False

        self.start_time = None
        self.last_apple_snake_info = {
            "snake_pos": [self.snake.pos.copy()],
            "snake_dir": self.snake.direction,
            "score": self.snake.star_snk_size-1  # starting score
        }
        self.moves_to_apple = 0
        # Generate the first apple
        self.apple = apple(size, [self.snake.pos.copy()], [0,0], 0)

        self.fill_sides()
        self.display_scores(prev_game_score)

    def loop(self):
        self.game_over = False
        started = False

        self.start_time = time.time()

        while self.game_over != True:
            self.screen.fill((35,38,117))
            self.snake.update()
            # Checks collisions of each block of the snake with the wall
            for x in self.blocks:
                if self.snake.check_collisions(x[1]) == True:
                    self.write_event('overW', other=dict(fin_pos=self.snake.get_snake_position()))
                    self.over(self.start_time)
                self.screen.blit(x[0],x[1])
            # Checks collisions of each block of the snake with the snake's mouth
            a=0
            for x in self.snake.images:
                if a !=0:
                    if self.snake.check_collisions2(x[1]) == True:
                        self.write_event('overS', other=dict(fin_pos=self.snake.get_snake_position()))

                        self.over(self.start_time)
                self.screen.blit(x[0],x[1])
                a+=1
            # # Checks collisions of the snake mouth with the apple
            if started and self.snake.check_apple(self.apple.pos) == True:
                # Writes the all info in the game log
                self.write_event('apple')
                snake_poss = self.snake.get_snake_position()
                # deletes  the old apple and creates a new one
                del self.apple
                self.apple = apple(self.size, snake_poss, self.snake.direction, self.snake.score)
                # Updates the info to save in the game log in the next apple
                self.last_apple_snake_info.update({
                    "snake_pos": snake_poss,
                    "snake_dir": self.snake.direction,
                    "score": self.snake.score
                })
                # Sets the moves to zero
                self.moves_to_apple = 0
                self.snake.add_apple()

            # Updates screen and checks for key presses
            self.screen.blit(self.apple.image,self.apple.pos)
            self.screen.blit(self.snake.image,self.snake.pos)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        if self.left is False and self.right is False:
                            self.reset()
                            self.snake.right()
                            self.right = True
                            self.moves_to_apple += 1

                    elif event.key == pg.K_LEFT:
                        if self.right is False and self.left is False:
                            self.reset()
                            self.snake.left()
                            self.left = True
                            self.moves_to_apple += 1

                    elif event.key == pg.K_UP:
                        if self.down is False and self.up is False:
                            self.reset()
                            self.snake.up()
                            self.up = True
                            self.moves_to_apple += 1

                    elif event.key == pg.K_DOWN:
                        if self.up is False and self.down is False:
                            self.reset()
                            self.snake.down()
                            self.down = True
                            self.moves_to_apple += 1

                    # Once the user presses the first key, we start the timer
                    # and save the info about the start of the game to the game log
                    if not started and (self.up or self.down or self.right or self.left):

                        self.start_time = time.time()
                        # We dont know the direction of the snake in the first apple of the game
                        self.last_apple_snake_info["snake_dir"] = [0, 0]
                        self.write_event('start')
                        # when the first apple is placed the score is zero
                        self.last_apple_snake_info["score"] = 0
                        started = True

            pg.display.update()

    def over(self, start_time):
        # restart with the same speed
        restart_same(self.snake.speed, self.size, self.snake.score)

    def reset(self):
        self.left,self.right,self.up,self.down = False,False,False,False

    def write_event(self, status, other=None):
        wrt_ap_sn = status != 'start'
        file.write(
            f"{status}|{time.time() - self.start_time:.03f}|{self.last_apple_snake_info['score']}|"
            f"{self.moves_to_apple if wrt_ap_sn else 0}|"
            f"{self.apple.pos if wrt_ap_sn else''}|{self.last_apple_snake_info['snake_pos'] if wrt_ap_sn else ''}|"
            f"{self.last_apple_snake_info['snake_dir'] if wrt_ap_sn else ''}|"
            f"{other if other else''}\n")

    def display_scores(self, prev_game_score):
        if prev_game_score is None:
            pg.display.set_caption('Snake Game')
        else:
            global best_score
            if prev_game_score > best_score:
                best_score = prev_game_score
            pg.display.set_caption(f"Snake Game - Last Score: {prev_game_score}"
                                   f"  (best: {best_score})")

    def fill_sides(self):
        color = (0, 0, 0)
        for x in range(0, SCR_SZ[0], 10):
            t = pg.Surface((10, 10))
            t.fill(color)
            self.blocks.append([t, [x, 0]])
        for x in range(0, SCR_SZ[0], 10):
            t = pg.Surface((10, 10))
            t.fill(color)
            self.blocks.append([t, [x, SCR_SZ[1] - 10]])
        for x in range(0, SCR_SZ[1], 10):
            t = pg.Surface((10, 10))
            t.fill(color)
            self.blocks.append([t, [0, x]])
        for x in range(0, SCR_SZ[1], 10):
            t = pg.Surface((10, 10))
            t.fill(color)
            self.blocks.append([t, [SCR_SZ[0] - 10, x]])

def start(speed,size, prev_game_score=None):
    global g,m
    try:
        del m
    except NameError:
        pass

    g=game(speed,size, prev_game_score)
    g.loop()

def restart_same(speed, size, prev_game_score):
    global m
    m = False
    start(speed, size, prev_game_score)

