# Simple terminal Tetris using curses
import curses
import random
import time

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TICK_RATE = 0.5  # seconds per drop step

# Tetromino shapes: orientations as list of lists of (x,y) offsets
SHAPES = {
    'I': [
        [(0,1), (1,1), (2,1), (3,1)],
        [(2,0), (2,1), (2,2), (2,3)],
        [(0,2), (1,2), (2,2), (3,2)],
        [(1,0), (1,1), (1,2), (1,3)],
    ],
    'J': [
        [(0,0), (0,1), (1,1), (2,1)],
        [(1,0), (2,0), (1,1), (1,2)],
        [(0,1), (1,1), (2,1), (2,2)],
        [(1,0), (1,1), (0,2), (1,2)],
    ],
    'L': [
        [(2,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (1,2), (2,2)],
        [(0,1), (1,1), (2,1), (0,2)],
        [(0,0), (1,0), (1,1), (1,2)],
    ],
    'O': [
        [(1,0), (2,0), (1,1), (2,1)],
        [(1,0), (2,0), (1,1), (2,1)],
        [(1,0), (2,0), (1,1), (2,1)],
        [(1,0), (2,0), (1,1), (2,1)],
    ],
    'S': [
        [(1,1), (2,1), (0,2), (1,2)],
        [(1,0), (1,1), (2,1), (2,2)],
        [(1,1), (2,1), (0,2), (1,2)],
        [(1,0), (1,1), (2,1), (2,2)],
    ],
    'T': [
        [(1,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (2,1), (1,2)],
        [(0,1), (1,1), (2,1), (1,2)],
        [(1,0), (0,1), (1,1), (1,2)],
    ],
    'Z': [
        [(0,1), (1,1), (1,2), (2,2)],
        [(2,0), (1,1), (2,1), (1,2)],
        [(0,1), (1,1), (1,2), (2,2)],
        [(2,0), (1,1), (2,1), (1,2)],
    ],
}

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - 2
        self.y = 0

    def cells(self, rotation=None, offset_x=None, offset_y=None):
        r = self.rotation if rotation is None else rotation
        ox = self.x if offset_x is None else offset_x
        oy = self.y if offset_y is None else offset_y
        return [(ox + x, oy + y) for x, y in SHAPES[self.shape][r]]

class Game:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        return Piece(random.choice(list(SHAPES.keys())))

    def valid(self, cells):
        for x, y in cells:
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def freeze_piece(self):
        for x, y in self.piece.cells():
            if y >= 0:
                self.board[y][x] = 1
        self.clear_lines()
        self.piece = self.new_piece()
        if not self.valid(self.piece.cells()):
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        cleared = BOARD_HEIGHT - len(new_board)
        self.score += cleared
        while len(new_board) < BOARD_HEIGHT:
            new_board.insert(0, [0] * BOARD_WIDTH)
        self.board = new_board

    def move(self, dx, dy, rotate=False):
        new_rot = (self.piece.rotation + 1) % 4 if rotate else self.piece.rotation
        cells = self.piece.cells(new_rot, self.piece.x + dx, self.piece.y + dy)
        if self.valid(cells):
            self.piece.rotation = new_rot
            self.piece.x += dx
            self.piece.y += dy
            return True
        return False

    def step(self):
        if not self.move(0, 1):
            self.freeze_piece()

    def draw(self, stdscr):
        stdscr.clear()
        # draw board
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val:
                    stdscr.addstr(y, x*2, '[]')
                else:
                    stdscr.addstr(y, x*2, '  ')
        # draw piece
        for x, y in self.piece.cells():
            if y >= 0:
                stdscr.addstr(y, x*2, '[]')
        stdscr.addstr(0, BOARD_WIDTH*2 + 2, f'Score: {self.score}')
        if self.game_over:
            stdscr.addstr(BOARD_HEIGHT//2, BOARD_WIDTH - 4, 'GAME OVER')
        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        last_time = time.time()
        while not self.game_over:
            ch = stdscr.getch()
            if ch == curses.KEY_LEFT:
                self.move(-1, 0)
            elif ch == curses.KEY_RIGHT:
                self.move(1, 0)
            elif ch == curses.KEY_DOWN:
                self.step()
            elif ch == ord(' '):
                self.move(0, 0, rotate=True)
            elif ch == ord('q'):
                break
            if time.time() - last_time > TICK_RATE:
                self.step()
                last_time = time.time()
            self.draw(stdscr)
        # final screen
        self.draw(stdscr)
        stdscr.nodelay(False)
        stdscr.getch()


def main():
    game = Game()
    curses.wrapper(game.run)


if __name__ == "__main__":
    main()
