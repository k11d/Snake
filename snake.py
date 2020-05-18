import numpy as np
import cv2
from graphics import Board

import time
from threading import Lock, Thread



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

    def update_body(self):
        for part in self.body:
            lastx, lasty = self._last_position
            self._last_position = [part.x, part.y]
            part.x = lastx
            part.y = lasty



class Player(Snake):
    def __init__(self, x, y, facing='S'):
        super().__init__(x, y, facing=facing)
        self.do_next_movement = lambda:None
    
    def set_colors(self, idname, color):
        if not hasattr(self, 'colors'):
            self.colors = {}
        _id = idname or '0'
        self.colors[_id] = color

    def left(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.x -= n
        if self.head.x < 0:
            self.head.x += self.right_border 

    def right(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.x = (self.head.x + n) % self.right_border

    def up(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.y -= n
        if self.head.y < 0:
            self.head.y += self.bot_border

    def down(self, n=1):
        self._last_position[0] = self.head.x
        self._last_position[1] = self.head.y
        self.head.y = (self.head.y + n) % self.bot_border
    
    def move(self, n=1):
        if self.facing == 'N':
            self.up()
        elif self.facing == 'S':
            self.down()
        elif self.facing == 'E':
            self.right()
        elif self.facing == 'W':
            self.left()
        self.update_body()



class World(Board):
    def draw_player(self, player):
        hx, hy = player.head.x, player.head.y
        self.fill(hx, hy, player.colors['head'])
        for part in player.body:
            self.fill(part.x, part.y, player.colors['body'])

    def wrap_outbound_player(self, player):
        px, py = player.head.x, player.head.y



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
    
    def set_world_borders(self):
        self.player.top_border = 0
        self.player.bot_border = self.world.rows
        self.player.left_border = 0
        self.player.right_border = self.world.cols

    def mainloop(self):
        t0 = time.time()
        while not self._quit:
            t1 = time.time()
            if t1 - t0 > self.speed_factor:
                t0 = t1
                self.player.move()

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                self.close()
                break

            elif k in self._keys.values():
                # print(k)
                if k == ord('g'):
                    self.player.grow()
                    self.player.move()
                elif k == ord('d'):
                    self.player.facing = 'E'
                elif k == ord('a'):
                    self.player.facing = 'W'
                elif k == ord('w'):
                    self.player.facing = 'N'
                elif k == ord('s'):
                    self.player.facing = 'S'
                elif k == ord('m'):
                    self.speed_factor += 0.01
                elif k == ord('n'):
                    self.speed_factor -= 0.01

            self.world.clear()
            self.world.draw_player(self.player)
            cv2.imshow('0', self.world._grid)



game = Game(
    Player(5, 5, 'S'),
    World(64, 64, 16, 16, (0, 0, 0))
)
game.set_world_borders()

p = game.player
p.set_colors('head', (0, 0, 255))
p.set_colors('body', (0,255,0))
game.mainloop()
