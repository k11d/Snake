import cv2
from graphics import Board
import time
import random



class SnakePart:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent


class SnakeHead(SnakePart):
    def __init__(self, x, y):
        super().__init__(x, y, parent=None)


class Snake:
    def __init__(self, x, y, facing='S'):
        self.head = SnakeHead(x, y)
        self._last_position = [x,y]
        self.facing = facing
        self.body = []

    def __repr__(self):
        s = f"[{self.head.x},{self.head.y}][{self.facing}]>\n"
        for p in self.body:
            s += f"[{p.x},{p.y}]\n"
        return s[:-1]

    def body_parts_positions(self):
        return (
            [p.x, p.y]
            for p in self.body
        )
    
    def grow(self):
        part = SnakePart(self.head.x, self.head.y, parent=self.head)
        self.body.append(part)

    def _left(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.x -= n
        if self.head.x < 0:
            self.head.x += self.right_border 

    def _right(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.x = (self.head.x + n) % self.right_border

    def _up(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.y -= n
        if self.head.y < 0:
            self.head.y += self.bot_border

    def _down(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.y = (self.head.y + n) % self.bot_border

    def move(self, n=1):
        if self.facing == 'N':
            self._up()
        elif self.facing == 'S':
            self._down()
        elif self.facing == 'E':
            self._right()
        elif self.facing == 'W':
            self._left()
        self.update_body()

    def update_body(self):
        for part in self.body:
            lastx, lasty = self._last_position
            self._last_position = [part.x, part.y]
            part.x = lastx
            part.y = lasty
    
    def is_biting_itself(self):
        for px, py in self.body_parts_positions():
            if px == self.head.x and py == self.head.y:
                return True
        return False


class Player(Snake):
    def __init__(self, x, y, facing='S'):
        super().__init__(x, y, facing=facing)
        self.x = x
        self.y = y
        self.score = 0

    def set_colors(self, idname, color):
        if not hasattr(self, 'colors'):
            self.colors = {}
        _id = idname or '0'
        self.colors[_id] = color
    
    def reset(self):
        self.score = 0
        self.body.clear()
        self.head.x = self.x
        self.head.y = self.y
        self._last_position = [self.head.x, self.head.y]


class Food:
    def __init__(self, x, y, color=(200, 30, 10), points=1):
        self.x = x
        self.y = y
        self.color = color
        self.points = points


class World(Board):
    def __init__(self, rows, cols, rowsize, colsize, bg_color):
        super().__init__(rows, cols, rowsize, colsize, bg_color)
        self.foods = []
    
    def reset(self):
        self.foods.clear()

    def draw_player(self, player):
        hx, hy = player.head.x, player.head.y
        self.fill(hx, hy, player.colors['head'])
        for part in player.body:
            self.fill(part.x, part.y, player.colors['body'])
    
    def draw_food(self):
        for f in self.foods:
            self.fill(f.x, f.y, f.color)

    def spawn_food(self):
        x = random.randint(0, self.cols - 1)
        y = random.randint(0, self.rows - 1)
        self.foods.append(Food(x,y))

    def is_colliding_food(self, player):
        return any(
            (player.head.x == f.x and player.head.y == f.y)
            for f in self.foods
        )


class Game:

    def __init__(self, player, world):
        self.player = player
        self.world = world
        self._quit = False
        self.speed_factor = 0.1
        self._keys = {k:w for k,w in zip(map(chr, range(32, 127)), range(32, 127))}

    def close(self):
        self._quit = True
        cv2.destroyAllWindows()
    
    def init_world(self):
        self.player.top_border = 0
        self.player.bot_border = self.world.rows
        self.player.left_border = 0
        self.player.right_border = self.world.cols
        self.world.spawn_food()
    
    def reset_game(self):
        self.player.reset()
        self.world.reset()
        self.init_world()

    def mainloop(self):
        t0 = time.time()
        while not self._quit:
            t1 = time.time()
            if t1 - t0 > self.speed_factor:
                t0 = t1
                self.player.move()
                self.world.clear()
                self.world.draw_player(self.player)
                self.world.draw_food()
                if self.player.is_biting_itself():
                    self.reset_game()
                    return self.mainloop()
                if self.world.is_colliding_food(self.player):
                    self.player.score += self.world.foods.pop().points
                    self.player.grow()
                    self.world.spawn_food()

            cv2.imshow('0', self.world._grid)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                self.close()
                break
            elif k in self._keys.values():
                if k == ord('g'):
                    self.player.grow()
                    self.player.move()
                elif k == ord('d'):
                    if self.player.facing != 'W':
                        self.player.facing = 'E'
                elif k == ord('a'):
                    if self.player.facing != 'E':
                        self.player.facing = 'W'
                elif k == ord('w'):
                    if self.player.facing != 'S':
                        self.player.facing = 'N'
                elif k == ord('s'):
                    if self.player.facing != 'N':
                        self.player.facing = 'S'
                elif k == ord('m'):
                    self.speed_factor += 0.01
                elif k == ord('n'):
                    self.speed_factor -= 0.01


if __name__ == '__main__':
    game = Game(
        Player(5, 5, 'S'),
        World(12, 12, 32, 32, (0, 0, 0))
    )
    game.player.set_colors('head', (0, 0, 255))
    game.player.set_colors('body', (0,255,0))
    game.init_world()
    game.mainloop()
