class Piece:
    def __init__(self, color):
        self.color = color  # 'w' or 'b'

    def symbol(self):
        raise NotImplementedError

    def moves(self, position, board):
        """Yield valid end positions for this piece from given position."""
        raise NotImplementedError


def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8


class Pawn(Piece):
    def symbol(self):
        return 'P' if self.color == 'w' else 'p'

    def moves(self, position, board):
        x, y = position
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        # forward move
        nx, ny = x + direction, y
        if in_bounds(nx, ny) and board[nx][ny] is None:
            yield (nx, ny)
            # double move from start
            if x == start_row:
                nx2 = x + 2 * direction
                if board[nx2][ny] is None:
                    yield (nx2, ny)
        # captures
        for dy in (-1, 1):
            nx, ny = x + direction, y + dy
            if in_bounds(nx, ny):
                piece = board[nx][ny]
                if piece is not None and piece.color != self.color:
                    yield (nx, ny)


class Rook(Piece):
    def symbol(self):
        return 'R' if self.color == 'w' else 'r'

    def moves(self, position, board):
        x, y = position
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x + dx, y + dy
            while in_bounds(nx, ny):
                piece = board[nx][ny]
                if piece is None:
                    yield (nx, ny)
                else:
                    if piece.color != self.color:
                        yield (nx, ny)
                    break
                nx += dx
                ny += dy


class Knight(Piece):
    def symbol(self):
        return 'N' if self.color == 'w' else 'n'

    def moves(self, position, board):
        x, y = position
        for dx, dy in ((2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)):
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny):
                piece = board[nx][ny]
                if piece is None or piece.color != self.color:
                    yield (nx, ny)


class Bishop(Piece):
    def symbol(self):
        return 'B' if self.color == 'w' else 'b'

    def moves(self, position, board):
        x, y = position
        for dx, dy in ((1,1),(1,-1),(-1,1),(-1,-1)):
            nx, ny = x + dx, y + dy
            while in_bounds(nx, ny):
                piece = board[nx][ny]
                if piece is None:
                    yield (nx, ny)
                else:
                    if piece.color != self.color:
                        yield (nx, ny)
                    break
                nx += dx
                ny += dy


class Queen(Piece):
    def symbol(self):
        return 'Q' if self.color == 'w' else 'q'

    def moves(self, position, board):
        # queen is rook + bishop
        for move in Rook.moves(self, position, board):
            yield move
        for move in Bishop.moves(self, position, board):
            yield move


class King(Piece):
    def symbol(self):
        return 'K' if self.color == 'w' else 'k'

    def moves(self, position, board):
        x, y = position
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny):
                    piece = board[nx][ny]
                    if piece is None or piece.color != self.color:
                        yield (nx, ny)
