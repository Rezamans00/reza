from typing import Optional, Tuple
from .board import (
    Piece, Pawn, Rook, Knight, Bishop, Queen, King, in_bounds
)


class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.to_move = 'w'
        self._setup_board()

    def _setup_board(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece_cls in enumerate(order):
            self.board[0][i] = piece_cls('b')
            self.board[7][i] = piece_cls('w')
        for i in range(8):
            self.board[1][i] = Pawn('b')
            self.board[6][i] = Pawn('w')

    def display(self):
        print('  a b c d e f g h')
        for i, row in enumerate(self.board):
            line = []
            for piece in row:
                line.append('.' if piece is None else piece.symbol())
            print(8-i, ' '.join(line), 8-i)
        print('  a b c d e f g h')
        print(f"Turn: {'White' if self.to_move == 'w' else 'Black'}")

    def parse(self, move: str) -> Optional[Tuple[Tuple[int,int], Tuple[int,int]]]:
        if len(move) != 4:
            return None
        cols = 'abcdefgh'
        try:
            sy = cols.index(move[0])
            sx = 8 - int(move[1])
            ty = cols.index(move[2])
            tx = 8 - int(move[3])
        except (ValueError, IndexError):
            return None
        if not in_bounds(sx, sy) or not in_bounds(tx, ty):
            return None
        return (sx, sy), (tx, ty)

    def is_in_check(self, color: str) -> bool:
        # find king position
        king_pos = None
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        if king_pos is None:
            return False
        # see if any enemy piece attacks king position
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None and piece.color != color:
                    for mx, my in piece.moves((x,y), self.board):
                        if (mx, my) == king_pos:
                            return True
        return False

    def make_move(self, move: str) -> bool:
        parsed = self.parse(move)
        if not parsed:
            print('Invalid input format. Use e2e4')
            return False
        (sx, sy), (tx, ty) = parsed
        piece = self.board[sx][sy]
        if piece is None:
            print('No piece at source square')
            return False
        if piece.color != self.to_move:
            print("Not your turn")
            return False
        legal = False
        for mx, my in piece.moves((sx, sy), self.board):
            if (mx, my) == (tx, ty):
                legal = True
                break
        if not legal:
            print('Illegal move')
            return False
        target = self.board[tx][ty]
        self.board[tx][ty] = piece
        self.board[sx][sy] = None
        if self.is_in_check(self.to_move):
            # undo move
            self.board[sx][sy] = piece
            self.board[tx][ty] = target
            print('Move would leave king in check')
            return False
        self.to_move = 'b' if self.to_move == 'w' else 'w'
        return True

    def has_moves(self, color: str) -> bool:
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None and piece.color == color:
                    for mx, my in piece.moves((x,y), self.board):
                        target = self.board[mx][my]
                        self.board[mx][my] = piece
                        self.board[x][y] = None
                        if not self.is_in_check(color):
                            self.board[x][y] = piece
                            self.board[mx][my] = target
                            return True
                        self.board[x][y] = piece
                        self.board[mx][my] = target
        return False

    def status(self):
        if self.is_in_check(self.to_move):
            if not self.has_moves(self.to_move):
                return 'checkmate'
            else:
                return 'check'
        else:
            if not self.has_moves(self.to_move):
                return 'stalemate'
        return 'ongoing'


def play():
    game = ChessGame()
    while True:
        game.display()
        status = game.status()
        if status == 'checkmate':
            winner = 'White' if game.to_move == 'b' else 'Black'
            print(f'Checkmate! {winner} wins.')
            break
        elif status == 'stalemate':
            print('Stalemate!')
            break
        elif status == 'check':
            print('Check!')
        move = input('Enter move (e.g., e2e4): ')
        if move.lower() in {'quit', 'exit'}:
            break
        game.make_move(move)


if __name__ == '__main__':
    play()
