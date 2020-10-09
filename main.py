import tkinter

WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


class Base:
    def correct_coords(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


class Piece(Base):
    def __init__(self, color):
        self.color = color
        self.count_of_moves = 0

    def char(self):
        return ''

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        return 0 <= row < 8 and 0 <= col < 8 \
               and (abs(row1 - row) + abs(col1 - col) > 0)

    def can_attack(self, board, row, col, row1, col1):
        if board.get_piece(row1, col1) is not None and board.get_piece(row1, col1).char() == 'K':
            return True


class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if col == col1 and board.get_piece(row1, col1) is not None:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1:
            return True
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def attack_na_prohode(self, board, row, col, row1, col1):
        piece = board.get_piece(row, col1)
        if self.color == WHITE and row == 4 and piece is not None and piece.char() == 'P' \
                and piece.count_of_moves == 1 and row1 == 5 and abs(col - col1) == 1 \
                or self.color == BLACK and row == 3 and piece is not None and piece.char() == 'P' \
                and piece.count_of_moves == 1 and row1 == 2 and abs(col - col1) == 1:
            return True

    def can_attack(self, board, row, col, row1, col1):
        if super().can_attack(board, row, col, row1, col1):
            return False
        direction = 1 if (self.color == WHITE) else -1
        if self.attack_na_prohode(board, row, col, row1, col1):
            return True
        if board.get_piece(row1, col1) is None or board.get_piece(row1, col1).color == self.color:
            return False
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Rook(Piece):
    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if not super().can_move(board, row, col, row1, col1):
            return False
        if row != row1 and col != col1 or row == row1 and col == col1:
            return False
        diff_col = abs(col - col1)
        diff_row = abs(row - row1)
        if not (row == row1 or col == col1 or diff_row == diff_col):
            return False
        if row < row1:
            row_d = 1
        elif row > row1:
            row_d = -1
        else:
            row_d = 0
        if col < col1:
            col_d = 1
        elif col > col1:
            col_d = -1
        else:
            col_d = 0
        x_row = row + row_d
        x_col = col + col_d
        while True:
            piece = board.get_piece(x_row, x_col)
            if x_row != row1 and x_col != col1:
                return False
            if x_row == row1 and x_col == col1:
                if piece is None or self.get_color() == opponent(piece.get_color()):
                    return True
                return False
            if piece is not None:
                return False
            x_row += row_d
            x_col += col_d

    def can_attack(self, board, row, col, row1, col1):
        if super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Knight(Piece):
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if not super().can_move(board, row, col, row1, col1):
            return False
        diff_col = abs(col1 - col)
        diff_row = abs(row1 - row)
        piece = board.field[row1][col1]
        if piece is not None:
            if piece.color != opponent(self.color):
                return False
        return diff_col == 2 and diff_row == 1 or diff_col == 1 and diff_row == 2

    def can_attack(self, board, row, col, row1, col1):
        if super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not super().can_move(board, row, col, row1, col1):
            return False
        d_row = 1 if (row1 >= row) else -1
        d_col = 1 if (col1 >= col) else -1
        diff_col = abs(col1 - col)
        diff_row = abs(row1 - row)
        if diff_col != diff_row:
            return False
        x_col = col + d_col
        x_row = row + d_row
        while True:
            piece = board.field[x_row][x_col]
            if piece is None:
                if abs(col1 - x_col) == abs(row1 - x_row):
                    return True
            else:
                if piece.get_color() == self.get_color():
                    return False
                elif x_row == row1 or x_col == col1:
                    return True
            x_col = col + d_col
            x_row = row + d_row

    def can_attack(self, board, row, col, row1, col1):
        if super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not super().can_move(board, row, col, row1, col1):
            return False
        diff_col = abs(col - col1)
        diff_row = abs(row - row1)
        if not (row == row1 or col == col1 or diff_row == diff_col):
            return False
        if row < row1:
            row_d = 1
        elif row > row1:
            row_d = -1
        else:
            row_d = 0
        if col < col1:
            col_d = 1
        elif col > col1:
            col_d = -1
        else:
            col_d = 0
        x_row = row + row_d
        x_col = col + col_d
        while True:
            piece = board.get_piece(x_row, x_col)
            if x_row == row1 and x_col == col1:
                if piece is None or self.get_color() == opponent(piece.get_color()):
                    return True
                return False
            if piece is not None:
                return False
            x_row += row_d
            x_col += col_d

    def can_attack(self, board, row, col, row1, col1):
        if super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class King(Piece):
    def left_castling_check(self, board):
        row = 0 if self.color == WHITE else 7
        king = board.field[row][4]
        rook = board.field[row][0]
        if rook is None or king is None:
            return False
        if king.count_of_moves != 0 or rook.count_of_moves != 0:
            return False
        if board.get_piece(row, 4).char() != King.char(King(board.color)) \
                or board.get_piece(row, 0).char() != Rook.char(Rook(board.color)):
            return False
        for i in range(1, 4):
            if board.get_piece(row, i) is not None:
                return False
        return True

    def left_castling(self, board):
        row = 0 if self.color == WHITE else 7
        board.move_piece(row, 0, row, 3)
        board.field[row][2] = board.field[row][4]
        board.field[row][4] = None

    def right_castling_check(self, board):
        row = 0 if self.color == WHITE else 7
        king = board.field[row][4]
        rook = board.field[row][7]
        if rook is None or king is None:
            return False
        if king.count_of_moves != 0 or rook.count_of_moves != 0:
            return False
        if board.get_piece(row, 4).char() != King.char(King(board.color)) \
                or board.get_piece(row, 7).char() != Rook.char(Rook(board.color)):
            return False
        for i in range(5, 7):
            if board.get_piece(row, i) is not None:
                return False
        return True

    def right_castling(self, board):
        row = 0 if self.color == WHITE else 7
        board.move_piece(row, 7, row, 5)
        board.field[row][6] = board.field[row][4]
        board.field[row][4] = None

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        row_castl = 0 if self.color == WHITE else 7
        if row1 == row_castl and col1 == 6 and self.right_castling_check(board) \
                or row1 == row_castl and col1 == 2 and self.left_castling_check(board):
            return True
        if not super().can_move(board, row, col, row1, col1) is False:
            return False
        if super().can_attack(board, row, col, row1, col1):
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None and piece.color == self.color:
            return False
        diff_col = abs(col - col1)
        diff_row = abs(row - row1)
        if diff_col == 2 and self.color == WHITE:
            king = board.field[0][4]
            rook = board.field[0][0]
            if rook is None:
                return False
            if king is None:
                return False
            if king.count_of_moves != 0 or rook.count_of_moves != 0:
                return False
            if board.get_piece(0, 4).char() != King.char(King(self.color)):
                return False
            if board.get_piece(0, 0).char() != Rook.char(Rook(self.color)):
                return False
            for i in range(1, 4):
                if board.get_piece(0, i) is not None:
                    return False
            if diff_col == 2 and diff_row == 0:
                return True
        if diff_col == 1 and diff_row == 0 or diff_col == 0 \
                and diff_row == 1 or diff_col == 1 and diff_row == 1:
            return True

    def can_attack(self, board, row, col, row1, col1):
        if self.can_move(board, row, col, row1, col1):
            return True


class Board(Base):
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        self.wk_coords = (0, 4)
        self.wk_check, self.bk_check = False, False
        self.bk_coords = (7, 4)

    def current_player_color(self):
        return self.color

    def move_and_promote_pawn(self, row, col, row1, col1):
        pawn = self.get_piece(row, col)
        piece = self.get_piece(row1, col1)
        if piece is not None:
            if pawn.get_color() == piece.get_color():
                return False
        if pawn is None or str(pawn.__class__.__name__) != 'Pawn' \
                or self.get_piece(row1, col1) is not None and col1 == col:
            return False
        if (not (pawn.can_attack(self, row, col, row1, col1))) \
                and not (pawn.can_move(self, row, col, row1, col1)):
            return False
        if row1 == 0 or row1 == 7:
            return True
        return False

    def get_piece(self, row, col):
        return self.field[row][col]

    def correct_coords(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if self.get_piece(row1, col1).char() == 'K':
            if self.get_piece(row1, col1).color == WHITE:
                self.wk_coords = (row1, col1)
            else:
                self.bk_coords = (row1, col1)
        self.color = opponent(self.color)
        piece.count_of_moves += 1
        return True


class GBoard(Board):
    def __init__(self, window, figures):
        self.window = window
        self.figures = figures
        self.canvas = None
        self.logger = None
        self.select = None
        self.view = None
        self.is_attacked = False
        self.is_moved = False
        self.promote_pawn = False
        self.elements = []
        self.col1, self.row1 = 0, 0
        self.pieces = {}
        self.prepare_and_start()

    def prepare_and_start(self):
        super().__init__()
        if self.canvas is not None:
            self.canvas.delete("all")
        else:
            self.canvas = tkinter.Canvas(
                self.window,
                bg='#FFFBE7',
                width=1000,
                height=840
            )
            self.canvas.bind("<ButtonPress>", self.mouse_press)
            self.canvas.pack()
        # Рисуем слева цифры
        self.canvas.create_line((
            (39, 0),
            (39, 800)
        ), fill="#000000")
        for i in range(1, 9):
            self.canvas.create_text(
                20,
                (i - 1) * 100 + 40,
                text=9 - i
            )
        # Рисуем снизу буквы
        self.canvas.create_line((
            (40, 801),
            (840, 801)
        ), fill="#000000")
        for i in range(1, 9):
            self.canvas.create_text(
                (i - 1) * 100 + 40 + 40,
                820,
                text=chr(64 + i)
            )
        # Рисуем место под фигуру
        self.canvas.create_rectangle((
            (840, 0),
            (1000, 300)
        ), fill="#FFFFFF")
        # Рисуем и очищаем Logger
        if self.logger is not None:
            self.logger.delete(0, 'end')
        else:
            self.logger = tkinter.Listbox(width=160, height=540)
            self.logger.place(x=840, y=300)
        self.quadros = []
        for row in range(8):
            self.quadros.append([None] * 8)
        self.pieces = {}
        for row in range(8):
            for col in range(8):
                self.quadros[row][col] = self.canvas.create_rectangle((
                    (col * 100 + 40, row * 100),
                    (col * 100 + 40 + 100, row * 100 + 100)
                ), fill='#FFFFFF')
        self.redraw_pieces()
        self.highlight()
        self.log('Игра началась')
        self.log('Ходят: ' + ('белые' if self.color == WHITE else 'черные'))

    def prom_pawn_draw(self):
        fillll = '#000000' if self.color == WHITE else '#FFFFFF'
        fillll1 = '#000000' if self.color == BLACK else '#FFFFFF'
        color = WHITE if self.color == WHITE else BLACK
        self.elements.append(self.canvas.create_rectangle(((220, 300), (620, 450)), fill=fillll))
        self.elements.append(self.canvas.create_line(((320, 300), (320, 450)), fill=fillll1))
        self.elements.append(self.canvas.create_line(((420, 300), (420, 450)), fill=fillll1))
        self.elements.append(self.canvas.create_line(((520, 300), (520, 450)), fill=fillll1))
        self.elements.append(self.canvas.create_image((220, 325),
                                                      image=self.figures[color]['N'], anchor='nw'))
        self.elements.append(self.canvas.create_image((320, 325),
                                                      image=self.figures[color]['R'], anchor='nw'))
        self.elements.append(self.canvas.create_image((420, 325),
                                                      image=self.figures[color]['Q'], anchor='nw'))
        self.elements.append(self.canvas.create_image((520, 325),
                                                      image=self.figures[color]['B'], anchor='nw'))

    def prom_pawn(self, event):
        x, y = event.x, event.y
        row, col = self.row1, self.col1
        self.redraw_pieces()
        char = self.get_piece_from_pawn(x, y)
        color = WHITE if self.color == BLACK else BLACK
        self.field[7 - row][col] = None
        if char == 'Q':
            self.field[7 - row][col] = Queen(color)
        elif char == 'B':
            self.field[7 - row][col] = Bishop(color)
        elif char == 'N':
            self.field[7 - row][col] = Knight(color)
        elif char == 'R':
            self.field[7 - row][col] = Rook(color)
        self.promote_pawn = False
        self.canvas.bind("<ButtonPress>", self.mouse_press)
        for el in self.elements:
            self.canvas.delete(el)
        self.redraw_pieces()

    def mouse_press(self, event):
        button, x, y = event.num, event.x, event.y
        if button != 1:
            return False
        position = self.get_row_and_col_from_xy(x, y)
        if position is None:
            return False
        row, col = position
        self.row1, self.col1 = row, col
        piece = self.get_piece(7 - row, col)
        self.is_attacked = False
        self.is_moved = False
        if self.select is not None:
            position = self.get_row_and_col_from_piece(self.select)
            if position is not None:
                c_row, c_col = position
                if self.move_and_promote_pawn(c_row, c_col, 7 - row, col):
                    self.canvas.bind("<ButtonPress>", self.prom_pawn)
                    self.prom_pawn_draw()
                if self.select.char() == 'P'\
                        and self.select.attack_na_prohode(board, c_row, c_col, 7 - row, col):
                    self.field[7 - row][col] = self.field[c_row][c_col]
                    self.field[c_row][c_col] = None
                    self.field[c_row][col] = None
                    self.color = opponent(self.color)
                    self.log('{}{} взята {}{}'.format(
                        'w' if self.select.get_color() == BLACK else 'b',
                        self.select.char(),
                        'w' if self.select.get_color() == WHITE else 'b',
                        self.select.char()
                    ))
                    self.is_moved = True

                elif self.select.char() == 'K' \
                        and (self.select.left_castling_check(board)
                             or self.select.right_castling_check(board)):
                    if col == 2 and self.select.left_castling_check(board):
                        self.select.left_castling(board)
                    elif col == 6 and self.select.right_castling_check(board):
                        self.select.right_castling(board)
                    self.log('Рокировка' + ('белого' if self.color == WHITE else 'чёрного')
                             + 'короля')
                    self.is_moved = True

                elif self.select.can_attack(self, c_row, c_col, 7 - row, col) and piece is not None:
                    self.move_piece(c_row, c_col, 7 - row, col)
                    self.log('{}{} взята {}{}'.format(
                        'w' if piece.get_color() == WHITE else 'b',
                        piece.char(),
                        'w' if self.select.get_color() == WHITE else 'b',
                        self.select.char()
                    ))
                    self.is_moved = True
                    self.is_attacked = True
                elif self.select.can_move(self, c_row, c_col, 7 - row, col):
                    self.move_piece(c_row, c_col, 7 - row, col)
                    self.log('{}{}: {}{} -> {}{}'.format(
                        'w' if self.select.get_color() == WHITE else 'b',
                        self.select.char(),
                        chr(65 + c_col),
                        c_row + 1,
                        chr(65 + col),
                        8 - row,
                    ))
                    self.is_moved = True
        if self.promote_pawn:
            self.prom_pawn(row, col)
        if self.is_moved is True:
            self.log('Ходят: ' + ('белые' if self.color == WHITE else 'черные'))
            self.select = None
            self.redraw_pieces()
            self.highlight()
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.select is not None:
            self.highlight()
        if self.view is not None:
            self.canvas.delete(self.view)
            self.view = None
        if self.select == piece:
            self.select = None
        else:
            self.view = self.canvas.create_image(
                (
                    870,
                    100
                ),
                image=self.figures[piece.get_color()][piece.char()],
                anchor='nw'
            )
            if self.is_attacked or self.promote_pawn:
                self.highlight(select=(row, col), steps=[])
                return
            self.select = piece
            steps = []
            for new_row in range(8):
                for new_col in range(8):
                    if piece.can_move(board, 7 - row, col, 7 - new_row, new_col) \
                            or piece.can_attack(board, 7 - row, col, 7 - new_row, new_col):
                        steps.append((new_row, new_col))
            self.highlight(select=(row, col), steps=steps)

    def highlight(self, select=None, steps=[]):
        for row in range(8):
            for col in range(8):
                self.canvas.itemconfig(
                    self.quadros[row][col],
                    fill='#FFFFFF' if (col + row) % 2 == 0 else '#000000'
                )
        if select is not None and len(select) == 2:
            row, col = select
            self.canvas.itemconfig(
                self.quadros[row][col],
                fill='#59CE65'
            )
        for step in steps:
            if step is not None and len(step) == 2:
                row, col = step
                self.canvas.itemconfig(
                    self.quadros[row][col],
                    fill='#D45106'
                )

    def redraw_pieces(self):
        for figure in self.pieces.values():
            self.canvas.delete(figure)
        self.pieces = {}
        for row in range(7, -1, -1):
            for col in range(0, 8):
                piece = self.get_piece(row, col)
                if piece is not None:
                    self.pieces[id(piece)] = self.canvas.create_image(
                        (
                            col * 100 + 40,
                            (7 - row) * 100
                        ),
                        image=self.figures[piece.get_color()][piece.char()],
                        anchor='nw'
                    )

    def get_row_and_col_from_xy(self, x, y):
        if x < 40 or x > 840 or y < 0 or y > 800:
            return None
        col = (x - 40) // 100
        row = y // 100
        return row, col

    def get_piece_from_pawn(self, x, y):
        shapes = {0: 'N', 1: 'R', 2: 'Q', 3: 'B'}
        if x < 220 or x > 620 or y < 300 or y > 450:
            return ''
        return shapes[(x - 220) // 100]

    def get_row_and_col_from_piece(self, piece):
        for row in range(8):
            for col in range(8):
                if self.field[row][col] == piece:
                    return row, col
        return None

    def log(self, text):
        if self.logger is not None:
            self.logger.insert(len(self.logger.keys()), text)


master = tkinter.Tk()
master.geometry(
    "{}x{}".format(
        1000,
        840
    )
)
x = (master.winfo_screenwidth() - 1000) / 2
y = (master.winfo_screenheight() - 840) / 2
master.wm_geometry("+%d+%d" % (x, y))
figures = {
    BLACK: {
        "P": tkinter.PhotoImage(file="figures/pawn_black.gif"),
        "R": tkinter.PhotoImage(file="figures/rook_black.gif"),
        "N": tkinter.PhotoImage(file="figures/knight_black.gif"),
        "B": tkinter.PhotoImage(file="figures/bishop_black.gif"),
        "Q": tkinter.PhotoImage(file="figures/queen_black.gif"),
        "K": tkinter.PhotoImage(file="figures/king_black.gif")
    },
    WHITE: {
        "P": tkinter.PhotoImage(file="figures/pawn_white.gif"),
        "R": tkinter.PhotoImage(file="figures/rook_white.gif"),
        "N": tkinter.PhotoImage(file="figures/knight_white.gif"),
        "B": tkinter.PhotoImage(file="figures/bishop_white.gif"),
        "Q": tkinter.PhotoImage(file="figures/queen_white.gif"),
        "K": tkinter.PhotoImage(file="figures/king_white.gif")
    }
}
board = GBoard(master, figures)
master.mainloop()
