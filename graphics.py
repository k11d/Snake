import numpy as np

class Board:
    def __init__(self, rows, cols, rowsize, colsize, bg_color):
        self.rows = rows
        self.cols = cols
        self.rowsize = rowsize
        self.colsize = colsize

        self.gheight= self.rows * self.rowsize
        self.gwidth = self.cols * self.colsize

        self.bg_color = bg_color
        self._grid = np.ndarray(shape=(self.gwidth, self.gheight, 3), dtype=np.uint8)
        self.clear()

    def fill(self, x, y, color):
        x0, y0 = x * self.colsize, y * self.rowsize
        x1, y1 = x0 + self.colsize, y0 + self.rowsize
        self._grid[y0:y1, x0:x1] = color

    def fillArea(self, x0, y0, x1, y1, color):
        for i in range(y0, y1):
            for j in range(x0, x1):
                self.fill(j, i, color)

    def clear(self):
        self.fillArea(0, 0, self.cols, self.rows, self.bg_color)


