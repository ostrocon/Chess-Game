from enum import Enum
import abc
import pygame as pg
import random


class Color(Enum):
    """
    Jack Bellgowan
    Enumeration class to hold a variable for two color of chess pieces
    """
    WHITE = 0
    BLACK = 1


class Piece(abc.ABC):
    """
    Jack Bellgowan, Connor Ostrowski, and Tim Lightner
    Abstract class for a piece of a chess game with the static variables image with is the
    file path for the png images. the static variable game so the pieces can keep track of the current game.

    Attributes:
        _board (list[list]): the board for the piece to be played on
        _color (Color): the Color of a piece can either be Black or White
    """
    # image path used to find sprite
    image = "./images/pieces.png"
    # _game is used to keep track of the current game
    _game = None
    SPRITESHEET = pg.image.load("images/pieces.png")

    def __init__(self, color: Color, board: list[list]):
        """
        Constructor for a piece class and takes the parameters color and a board
        """
        self._board = board
        self._color = color
        self._image = pg.Surface((105, 105), pg.SRCALPHA)

    @staticmethod
    def set_game(game):
        """
        Setter for the game attribute

        Parameters:
             game: the current game the pieces belong to

        Raises:
            ValueError: when the new game is not a Game instance there will be an error
        """
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    @property
    def color(self) -> Enum:
        """
        getter for the game attribute

        Returns:
            _game: the current game the pieces are a part of
        """
        return self._color

    def set_image(self, x: int, y: int) -> None:
        """
        will take an x and y from the images file and will copy into a 105x105 pixel chunk into
        the current pieces image

        Parameters:
            x (int): the x coordinate for the piece in the file
            y (int): the y coordinate for the piece in the file
        """
        # take an x and y value and copy from the image file a 105x105 pixel chunk into the current piece's image
        self._image.blit(Piece.SPRITESHEET, (0, 0), pg.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        # checks for possible diagonal moves with a given vector
        """
        will take a given position using x and y on the board and find all the valid diagonal moves for a piece.
        The direction of the board is given used a vector y_d and x_d and -1 or 1 for each vector.
        Will check to the end of the board unless there is a piece blocking its path and which it must check the color
        If the color is the same the current piece must stop one less than its same color and if the color is opposite it
        take the other piece position and capture it.

        Parameters:
            y (int): the y position on the board
            x (int): the x position on the board
            y_d (int): the y vector direction
            x_d (int): the x vector direction
            distance (int): how for to check from the current piece direction

        Raises:
            ValueError: in the vector direction in not diagonal this error will be raised

        Returns:
            moves (list[tuple[int,int]]): the positions that a piece can move in a vertical direction
        """
        # checks for possible diagonal moves with a given vector
        moves: list = []
        if x_d not in (-1,1) or y_d not in (-1,1) or distance < 1 or not 0<=x<=7 or not 0<=y<=7:
            raise ValueError("Invalid input for diagonal move")
        for num in range(1, distance+1):
            x_num, y_num = num*x_d, num*y_d
            if not 0<=x+x_num<=7 or not 0<=y+y_num<=7:
                continue
            # if the spot is empty
            if not self._board[x+x_num][y+y_num]:
                moves.append((y+y_num,x+x_num))
            else:
                # if spot is an enemy
                if self._board[x + x_num][y+y_num].color != self.color:
                    moves.append((y + y_num, x + x_num))
                    return moves
                # if spot is not an enemy
                return moves
        return moves

    def _horizontal_moves(self, y: int, x: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """
         will take a given position using x and y on the board and find all the valid diagonal moves for a piece.
        The direction of the board is given used a vector y_d and x_d and -1 or 1 for each vector.
        Will check to the end of the board unless there is a piece blocking its path and which it must check the color
        If the color is the same the current piece must stop one less than its same color and if the color is opposite it
        take the other piece position and capture it.

        Parameters:
            y (int): the y position on the board
            x (int): the x position on the board
            y_d (int): the y vector direction
            x_d (int): the x vector direction
            distance (int): how for to check from the current piece direction

        Raises:
            ValueError: in the vector direction in not horizontal this error will be raised

        Returns:
            moves (list[tuple[int,int]]): the positions that a piece can move in a vertical direction
        """
        # checks for possible horizontal moves with a given vector
        moves: list = []
        if x_d not in (-1,1) or distance < 1 or not 0<=x<=7 or not 0<=y<=7:
            raise ValueError("Invalid input for horizontal move")
        for num in range(x_d,(distance*x_d)+x_d,x_d):
            # if pos is in range
            if 0<= x+num <= 7:
                # if spot is empty
                if not self._board[x+num][y]:
                    moves.append((y,x+num))
                # if spot is not empty
                else:
                    # if spot is an enemy
                    if self._board[x+num][y].color != self.color:
                        moves.append((y, x + num))
                        return moves
                    # if spot is not an enemy
                    return moves
            else:
                # pos is out of range
                return moves
        return moves

    def _vertical_moves(self, y: int, x: int, y_d: int, distance: int) -> list[tuple[int, int]]:
        """
        will take a given position using x and y on the board and find all the valid diagonal moves for a piece.
        The direction of the board is given used a vector y_d and x_d and -1 or 1 for each vector.
        Will check to the end of the board unless there is a piece blocking its path and which it must check the color
        If the color is the same the current piece must stop one less than its same color and if the color is opposite it
        take the other piece position and capture it.

        Parameters:
            y (int): the y position on the board
            x (int): the x position on the board
            y_d (int): the y vector direction
            x_d (int): the x vector direction
            distance (int): how for to check from the current piece direction

        Raises:
            ValueError: in the vector direction in not horizontal this error will be raised

        Returns:
            moves (list[tuple[int,int]]): the positions that a piece can move in a vertical direction
        """
        moves: list = []
        if y_d not in (-1, 1) or distance < 1 or not 0 <= x <= 7 or not 0 <= y <= 7:
            raise ValueError("Invalid input for vertical move")
        for num in range(y_d, (distance * y_d)+y_d, y_d):
            # if pos is in range
            if 0 <= y + num <= 7:
                # if spot is empty
                if not self._board[x][y + num]:
                    moves.append((y + num, x))
                # if spot is not empty
                else:
                    # if spot is an enemy
                    if self._board[x][y + num].color != self.color:
                        moves.append((y + num, x))
                        return moves
                    # if spot is not an enemy
                    return moves
            else:
                # pos is out of range
                return moves
        return moves

    @abc.abstractmethod
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        valid_moves in an abstract method that will return all the valid moves for a piece at a given location

        Parameters:
            y (int): The y coordinate of the piece
            x (int): The x coordinate of the piece

        Returns:
            list[tuple[int,int]]
        """
        pass

    @abc.abstractmethod
    def copy(self):
        """
        the function will copy a piece and is used to simulate possible moves for the computer
        """
        pass


class King(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The king piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the king piece
        board (list[list]]): the current baord for the game
    """

    def __init__(self, color: Color, board: list[list]) -> None:
        """
        Constructor for the king class and calls the set_image method to get an image for the kind

        Parameters:
            color (Color): the color of the king piece
            board (list[list]]): the current baord for the game
        """
        super().__init__(color, board)
        super().set_image(0, 0  if self.color == Color.WHITE else 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the king which is 1 in any of the
        eight directions

        Parameters:
            y (int): the y coordinate for the king
            x (int): the x coordinate for the king

        Returns:
            moves (list[tuple[int,int]]): the moves for the current kings position
        """
        moves = []
        for direction in range(-1,2,2):
            moves += super()._vertical_moves(y,x,direction,1)
            moves += super()._horizontal_moves(y,x,direction,1)
            for diagonal_num in range(-1,2,2):
                moves += super()._diagonal_moves(y,x,direction,diagonal_num,1)
        return moves

    def copy(self) -> Piece:
        """
        will return a new king of the same color

        Returns:
            King (Piece): same king piece of the current game
        """
        return King(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board)


class Queen(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The Queen piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the Queen piece
        board (list[list]]): the current board for the game
    """

    def __init__(self, color: Color, board: list[list]) -> None:
        """
        Constructor for the Queen class and calls the set_image method to get an image for the queen

        Parameters:
            color (Color): the color of the Queen piece
            board (list[list]]): the current board for the game
        """
        super().__init__(color, board)
        super().set_image(105, 0 if self.color == Color.WHITE else 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the queen which can move n amount of the
        eight directions

        Parameters:
            y (int): the y coordinate for the queen
            x (int): the x coordinate for the queen

        Returns:
            moves (list[tuple[int,int]]): the moves for the current queen position
        """
        moves = []
        for direction in range(-1, 2, 2):
            moves += super()._vertical_moves(y, x, direction, 8)
            moves += super()._horizontal_moves(y, x, direction, 8)
            for diagonal_num in range(-1, 2, 2):
                moves += super()._diagonal_moves(y, x, direction, diagonal_num, 8)
        return moves

    def copy(self) -> Piece:
        """
        will return a new queen of the same color

        Returns:
            Queen (Piece): same queen piece of the current game
        """
        return Queen(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board)


class Bishop(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The Bishop piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the Bishop piece
        board (list[list]]): the current board for the game
    """
    def __init__(self, color: Color, board: list[list]) -> None:
        """
        Constructor for the bishop class and calls the set_image method to get an image for the bishop

        Parameters:
            color (Color): the color of the bishop piece
            board (list[list]]): the current board for the game
        """
        super().__init__(color, board)
        super().set_image(210, 0 if self.color == Color.WHITE else 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the bishop which can move n amount but
        only in the diagonal

        Parameters:
            y (int): the y coordinate for the Bishop
            x (int): the x coordinate for the Bishop

        Returns:
            moves (list[tuple[int,int]]): the moves for the current Bishop position
        """
        moves = []
        for direction in range(-1, 2, 2):
            for diagonal_num in range(-1, 2, 2):
                moves += super()._diagonal_moves(y, x, direction, diagonal_num, 8)
        return moves

    def copy(self) -> Piece:
        """
        will return a new bishop of the same color

        Returns:
            bishop (Piece): same bishop piece of the current game
        """
        return Bishop(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board)


class Knight(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The Knight piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the Knight piece
        board (list[list]]): the current board for the game
    """
    def __init__(self, color: Color, board: list[list]) -> None:
        """
        Constructor for the Knight class and calls the set_image method to get an image for the Knight

        Parameters:
            color (Color): the color of the Knight piece
            board (list[list]]): the current board for the game
        """
        super().__init__(color, board)
        super().set_image(315, 0 if self.color == Color.WHITE else 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the Knight which can only move in a L
        shape either 2 vertically and one to the side or two to the side and one vertical

        Parameters:
            y (int): the y coordinate for the Knight
            x (int): the x coordinate for the Knight

        Returns:
            moves (list[tuple[int,int]]): the moves for the current Knight position
        """
        moves: list = []
        # up
        if not y - 2 < 0:
            for direction in range(-1, 2, 2):
                try:
                    if not 0 <= x + direction <= 7:
                        raise IndexError
                    item = self._board[x + direction][y - 2]
                except IndexError:
                    continue
                else:
                    if not item or (item and item.color != self.color):
                        moves.append((y - 2, x + direction))
        # right
        if not x + 2 > 7:
            for direction in range(-1, 2, 2):
                try:
                    if not 0 <= y + direction <= 7:
                        raise IndexError
                    item = self._board[x + 2][y + direction]
                except IndexError:
                    continue
                else:
                    if not item or (item and item.color != self.color):
                        moves.append((y + direction, x + 2))
        # down
        if not y + 2 > 7:
            for direction in range(-1, 2, 2):
                try:
                    if not 0 <= x + direction <= 7:
                        raise IndexError
                    item = self._board[x + direction][y + 2]
                except IndexError:
                    continue
                else:
                    if not item or (item and item.color != self.color):
                        moves.append((y + 2, x + direction))
        # left
        if not x - 2 < 0:
            for direction in range(-1, 2, 2):
                try:
                    if not 0 <= y + direction <= 7:
                        raise IndexError
                    item = self._board[x - 2][y + direction]
                except IndexError:
                    continue
                else:
                    if not item or (item and item.color != self.color):
                        moves.append((y + direction, x - 2))
        return moves

    def copy(self) -> Piece:
        """
        will return a new Knight of the same color

        Returns:
            Knight (Piece): same Knight piece of the current game
        """
        return Knight(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board)


class Rook(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The Rook piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the Rook piece
        board (list[list]]): the current board for the game
    """
    def __init__(self, color: Color, board: list[list]) -> None:
        """
        Constructor for the Rook class and calls the set_image method to get an image for the Rook

        Parameters:
            color (Color): the color of the Rook piece
            board (list[list]]): the current board for the game
        """
        super().__init__(color, board)
        super().set_image(420, 0 if self.color == Color.WHITE else 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the Rook which can only move vertically
        or horizontally as many as they can

        Parameters:
            y (int): the y coordinate for the Rook
            x (int): the x coordinate for the Rook

        Returns:
            moves (list[tuple[int,int]]): the moves for the current Rook position
        """
        moves = []
        for direction in range(-1, 2, 2):
            moves += super()._vertical_moves(y, x, direction, 8)
            moves += super()._horizontal_moves(y, x, direction, 8)
        return moves

    def copy(self) -> Piece:
        """
        will return a new Rook of the same color

        Returns:
            Rook (Piece): same Rook piece of the current game
        """
        return Rook(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board)


class Pawn(Piece):
    """
    Jack Bellgowan and Tim Lightner and Connor Ostrowski

    The Pawn piece inherits from the piece abstract base class and will create a unique piece for the game

    Attributes:
        color (Color): the color of the Pawn piece
        board (list[list]]): the current board for the game
    """
    def __init__(self, color: Color, board: list[list], first_move: bool = True) -> None:
        """
        Constructor for the Pawn class and calls the set_image method to get an image for the Pawn

        Parameters:
            color (Color): the color of the Pawn piece
            board (list[list]]): the current board for the game
        """
        super().__init__(color, board)
        self._first_move: bool = first_move
        super().set_image(525, 0 if self.color == Color.WHITE else 105)

    @property
    def first_move(self) -> bool:
        """
        first move property getter

        Returns:
            _first_move (bool): determines weather a pawn has moved
        """
        return self._first_move

    @first_move.setter
    def first_move(self, val: bool) -> None:
        """
        first move property setter

        Parameter:
            val (bool): the new val for the first move property

        Returns:
             _first_move (bool): the new value of the property
        """
        self._first_move = val

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        the abstract method that is created here to collect the valid moves for the Pawn which can move two or one
        in the direction towards the opposite color. if there is a piece diagonal from it the pawn can move and capture
        it. Also, when it reaches the other side of the board it turns into a queen.

        Parameters:
            y (int): the y coordinate for the Pawn
            x (int): the x coordinate for the Pawn

        Returns:
            moves (list[tuple[int,int]]): the moves for the current pawn position
        """
        moves = []
        # if player is moving a pawn
        if self.color == Color.WHITE:
            # adds vertical moves
            if y > 0 and not self._board[x][y - 1]:
                dist = 2 if ((self._board[x][y - 2] is None) if self._first_move else False) else 1
                moves += super()._vertical_moves(y, x, -1, dist)
            # adds horizontal moves if there is a piece there
            if x == 0 and self._board[x + 1][y - 1] and self._board[x + 1][y - 1].color != self.color:
                moves += super()._diagonal_moves(y, x, -1, 1, 1)
            elif x == 7 and self._board[x - 1][y - 1] and self._board[x - 1][y - 1].color != self.color:
                moves += super()._diagonal_moves(y, x, -1, -1, 1)
            elif 0 < x < 7:
                for direction in range(-1, 2, 2):
                    if self._board[x + direction][y - 1] and self._board[x + direction][y - 1].color != self.color:
                        moves += super()._diagonal_moves(y, x, -1, direction, 1)
        # if AI is moving pawn
        else:
            # adds vertical moves
            if y > 0 and not self._board[x][y + 1]:
                dist = 2 if ((self._board[x][y + 2] is None) if self._first_move else False) else 1
                moves += super()._vertical_moves(y, x, 1, dist)
            # adds horizontal moves if there is a piece there
            if x == 0 and self._board[x + 1][y + 1] and self._board[x + 1][y + 1].color != self.color:
                moves += super()._diagonal_moves(y, x, 1, 1, 1)
            elif x == 7 and self._board[x - 1][y + 1] and self._board[x - 1][y + 1].color != self.color:
                moves += super()._diagonal_moves(y, x, 1, -1, 1)
            elif 0 < x < 7:
                for direction in range(-1, 2, 2):
                    if self._board[x + direction][y + 1] and self._board[x + direction][y + 1].color != self.color:
                        moves += super()._diagonal_moves(y, x, 1, direction, 1)
        return moves

    def copy(self) -> Piece:
        """
        will return a new pawn of the same color

        Returns:
            Pawn (Piece): same pawn piece of the current game
        """
        return Pawn(Color.BLACK if self.color == Color.BLACK else Color.WHITE, self._board, self._first_move)


class Game:
    def __init__(self) -> None:
        """
        Jack Bellgowan and Tim Lightner and Connor Ostrowski
        sets the default state of the game,
        it sets _current_player to white,
        it sets the default board and makes the _boardStack

        Returns: None
        """
        self._current_player: Color = Color.WHITE
        self.setBoardDefault()
        self._boardStack: Game.BoardStack = Game.BoardStack()

    @property
    def current_player(self) -> Color:
        """
        Getter for ._current_player
        returns:
        _current_player (Color): the user will have the color WHITE
        """
        return self._current_player

    @property
    def board(self) -> list[list]:
        """
        getter for _board
        returns:
        _board: (list[list]) : the current state of the board game
        """
        return self._board

    def setBoardDefault(self) -> None:
        """
        Sets board in default state
        returns: None
        """
        # makes a 2x2 list and sets each value to None
        self._current_player = Color.WHITE
        # sets board to 2d 8x8 list of None
        self._board: list[list] = [[None for _ in range(8)] for _ in range(8)]
        # places pieces in default locations
        self._setup_pieces()

    def _setup_pieces(self) -> None:
        """
        Creates all default piece objects, and sets them to the default locations
        returns None
        """
        # First create all the pieces
        wk = King(Color.WHITE, self._board)
        bk = King(Color.BLACK, self._board)
        wq = Queen(Color.WHITE, self._board)
        bq = Queen(Color.BLACK, self._board)
        wr1 = Rook(Color.WHITE, self._board)
        wr2 = Rook(Color.WHITE, self._board)
        br1 = Rook(Color.BLACK, self._board)
        br2 = Rook(Color.BLACK, self._board)
        wn1 = Knight(Color.WHITE, self._board)
        wn2 = Knight(Color.WHITE, self._board)
        bn1 = Knight(Color.BLACK, self._board)
        bn2 = Knight(Color.BLACK, self._board)
        wb1 = Bishop(Color.WHITE, self._board)
        wb2 = Bishop(Color.WHITE, self._board)
        bb1 = Bishop(Color.BLACK, self._board)
        bb2 = Bishop(Color.BLACK, self._board)
        wp0 = Pawn(Color.WHITE, self._board)
        wp1 = Pawn(Color.WHITE, self._board)
        wp2 = Pawn(Color.WHITE, self._board)
        wp3 = Pawn(Color.WHITE, self._board)
        wp4 = Pawn(Color.WHITE, self._board)
        wp5 = Pawn(Color.WHITE, self._board)
        wp6 = Pawn(Color.WHITE, self._board)
        wp7 = Pawn(Color.WHITE, self._board)
        bp0 = Pawn(Color.BLACK, self._board)
        bp1 = Pawn(Color.BLACK, self._board)
        bp2 = Pawn(Color.BLACK, self._board)
        bp3 = Pawn(Color.BLACK, self._board)
        bp4 = Pawn(Color.BLACK, self._board)
        bp5 = Pawn(Color.BLACK, self._board)
        bp6 = Pawn(Color.BLACK, self._board)
        bp7 = Pawn(Color.BLACK, self._board)

        # Then set them at the correct spots
        row0 = [br1, bn1, bb1, bq, bk, bb2, bn2, br2]
        row1 = [bp0, bp1, bp2, bp3, bp4, bp5, bp6, bp7]
        row6 = [wp0, wp1, wp2, wp3, wp4, wp5, wp6, wp7]
        row7 = [wr2, wn1, wb1, wq, wk, wb2, wn2, wr1]

        # places the rows on the board in correct order
        for i in range(0, 8):
            self._board[i][0] = row0[i]
            self._board[i][1] = row1[i]
            self._board[i][6] = row6[i]
            self._board[i][7] = row7[i]

    def get(self, y: int, x: int) -> any:
        """
        Accepts y as an int for desired y value on board and x as an int for desired y value on board
        returns None or an item of type Piece

        Parameters:
            y (int): the y position of the piece
            x (int): the x position of the piece

        Returns:
            _board (any): can return a piece type or none depending if a piece is at a location
        """
        if 0 <= x <= 7 and 0 <= y <= 7:
            return self._board[x][y]

    def switch_player(self) -> None:
        """
        swaps self._current_player to the other color
        returns: None
        """
        self._current_player = Color.BLACK if self._current_player == Color.WHITE else Color.WHITE

    def reset(self) -> None:
        """
        Resets the board to the default state
        returns: None
        """
        # sets board to default
        self.setBoardDefault()

    def undo(self, player_called: bool = True) -> bool:
        """
        undo will allow a player to erase their last move and will move the piece and the black piece
        back to the position it was before

        Returns:
            bool: if an undo operation can be done.
        """
        # checks if an item can be popped
        if self._boardStack.length() != 0:
            self.switch_player()
            # sets the board to last state
            self._board = self._boardStack.pop()
            # success undoing
            if player_called:
                self.undo(False)
            return True
        self._current_player = Color.WHITE
        # failure undoing
        return False

    def copy_board(self) -> list[list]:
        """
        this allows the Ai to determine all moves without changing any pieces on the
        board that the player sees

        Returns:
            new_board (list[list]): the current state of the board with the pieces in place
        """
        # makes a new board variable
        new_board: list = []
        # loops over each column
        for col in self._board:
            # makes a new row variable
            new_row = []
            # for each piece in each column
            for piece in col:
                # if there is a piece at the location
                if piece:
                    # if piece is a pawn
                    if isinstance(piece, Pawn):
                        # moves a copy of the pawn to the new row
                        new_row.append(Pawn(piece.color, new_board, piece.first_move))
                    else:
                        # creates a piece of the correct type to add to the row
                        piece_type = type(piece)
                        # adds the new row to the new board
                        new_row.append(piece_type(piece.color, new_board))
                else:
                    # adds None to the row
                    new_row.append(None)
            # adds row to board
            new_board.append(new_row)
        return new_board


    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """
        will first copy the board and then set a new location for a piece and then will
        remove the old position It will return a bool that is if the new state will put the player
        in check and if it does then the move can not happen. No move can be done if it puts the
        player in check.

        Parameters:
            piece (Piece): the piece that will be moved
            y (int): the old y position of the piece
            x (int): the old x position of the piece
            y2 (int): the new y position of the piece
            x2 (int): the new x position of the piece

        Returns:
            bool: if the play does or does not put the player in check
        """
        # copies board onto stack
        self._boardStack.push(self.copy_board())
        # sets old location to None
        self._board[x][y] = None
        # checks if piece is a pawn for special behavior
        if isinstance(piece, Pawn):
            # sets first move to false for 2 space first move
            piece.first_move = False
            # changes pawn to a queen logic for each color
            if piece.color == Color.WHITE and y2 == 0:
                self._board[x2][y2] = Queen(Color.WHITE, self._board)
            elif piece.color == Color.BLACK and y2 == 7:
                self._board[x2][y2] = Queen(Color.BLACK, self._board)
            else:
                # if it is a pawn, and it is not in the last row
                self._board[x2][y2] = piece
        else:
            # if piece is not a pawn
            self._board[x2][y2] = piece
        # if move results in check
        if self.check(piece.color):
            # undoes move
            self.undo(False)
            self.switch_player()
            # returns false for invalid move
            return False
        # switches player turn
        self.switch_player()
        # successful move
        return True

    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """
        this method will find the all of the locations of a ceritan color

        Parameters:
            color (Color): the color of pieces to find

        Returns:
            piece_list (list[tuple[int,int]]): all locations of pieces of a certian color
        """
        # returns in form (Y,X)
        piece_list = []
        # loops over each current row
        for n_col, col in enumerate(self._board):
            # loops over each current item
            for n_row, item in enumerate(col):
                # checks if the item is the correct color
                if item and item.color == color:
                    piece_list.append((n_row, n_col))
        # returns the list
        return piece_list

    def find_king(self, color: Color) -> tuple[int, int]:
        """
        this method will find the King of a given color

        Parameters:
            color (Color): which king in the game to find

        Returns:
            piece_location (tuple[int,int]): the position of the king
        """

        # gets locations of pieces
        locations = self.get_piece_locations(color)
        # checks each piece
        for piece_location in locations:
            if isinstance(self.get(piece_location[0], piece_location[1]), King):
                # checks if the piece is of type King
                return piece_location

    def check(self, color: Color) -> bool:
        """
        check will determine if the possible moves of the color will put the other king in check
        it uses the current positions and valid_moves() to see if any moves will complete this action
        Parameters:
            color (Color): which color to check if a king is in check

        Returns:
            bool: returns true or false if a king is in check
        """
        # sets the enemy color to the opposite of its own
        enemy_color = Color.BLACK if color == Color.WHITE else color.WHITE
        # gets all the enemy piece locations as tuple(y, x) and puts them in the list
        enemy_pieces_list = self.get_piece_locations(enemy_color)
        king = self.find_king(color)
        # Finds what class of piece each location is and makes a list of their valid moves
        for piece in enemy_pieces_list:
            if king in self.get(piece[0], piece[1]).valid_moves(piece[0], piece[1]):
                return True
        # returns false
        return False


    def mate(self, color: Color) -> bool:
        """
        will see if a given color will check if a king is in check and there are no more moves for a king
        to complete. if that is the case the game will be over. It calls the check method and finds all
        the possible moves to determine if a king can escape and not be in check.

        Parameters:
            color (Color): the color of the king

        Returns:
            bool: if the king of the color parameter is in check 
        """
        # checks if king is in check
        if not self.check(color):
            return False
        # gets king and possible king moves
        king = self.find_king(color)
        king_moves = self.get(king[0], king[1]).valid_moves(king[0], king[1])
        # loops through each move
        for king_move in king_moves:
            # tries each move to see if the king is in check
            self.move(self.get(king[0], king[1]), king[0], king[1], king_move[0], king_move[1])
            # returns false and undoes the move if the king is in not in check
            if not self.check(color):
                self.undo(False)
                return False
        for piece in self.get_piece_locations(color):
            for move in self.get(piece[0], piece[1]).valid_moves(piece[0], piece[1]):
                self.move(self.get(piece[0], piece[1]), piece[0], piece[1], move[0], move[1])
                # returns false and undoes the move if the king is in not in check
                if not self.check(color):
                    self.undo(False)
                    return False
        return True

    def _computer_move(self):
        """
        Computer over helps the AI to play smarter by giving a set a rules to play by. It will first determine what moves
        are avaible to move the black pieces. it will then choose to move in the following order: checkmate, check, capture
        a queen, capture a bishop, capture knight, capture rook, capture a pawn, if it can not capture any white pieces
        it will preform a rando move.

        Returns: None
        """
        assert self.current_player == Color.BLACK
        # value of each move
        moves = {
            "MATE": 7,
            "CHECK": 6,
            "QUEEN": 5,
            "BISHOP": 4,
            "KNIGHT": 3,
            "ROOK": 2,
            "PAWN": 1,
            "RANDOM": 0,
        }
        best_move = moves["RANDOM"]
        move_data = None
        # if Black is in check
        if self.check(Color.BLACK):
            # find the black king
            king = self.find_king(Color.BLACK)
            king_moves = self.get(king[0], king[1]).valid_moves(king[0], king[1])
            # loops through each move
            for king_move in king_moves:
                # tries each move to see if the king is in check
                self.move(self.get(king[0], king[1]), king[0], king[1], king_move[0], king_move[1])
                # returns false and undoes the move if the king is in not in check
                if not self.check(Color.BLACK):
                    return f"BLACK is in CHECK!\nBLACK moved King\n"
            for piece in self.get_piece_locations(Color.BLACK):
                for move in self.get(piece[0], piece[1]).valid_moves(piece[0], piece[1]):
                    piece_type = self.get(piece[0], piece[1])
                    self.move(piece_type, piece[0], piece[1], move[0], move[1])
                    # returns false and undoes the move if the king is in not in check
                    if not self.check(Color.BLACK):
                        return f"BLACK is in CHECK!\nBLACK moved {piece_type.__class__.__name__}\n"
        for cords in self.get_piece_locations(Color.BLACK):
            # get piece
            piece = self.get(cords[0], cords[1])
            # every move that piece can make
            current_moves = piece.valid_moves(cords[0], cords[1])
            # loop through every move
            for move in current_moves:
                # get piece captured
                spot_taken = self.get(move[0], move[1])
                # check for self mate or check
                if self.move(piece, cords[0], cords[1], move[0], move[1]):
                    # check for enemy mate
                    if self.mate(Color.WHITE):
                        # new best move
                        move_data = (piece, move, cords)
                        best_move = moves["MATE"]
                    # check for enemy check
                    elif self.check(Color.WHITE) and best_move <= 6:
                        # new best move
                        move_data = (piece, move, cords)
                        best_move = moves["CHECK"]
                    # undo board
                    self.undo(False)
                else:
                    # the move will lead to check or checkmate
                    continue
                # move will take queen
                if isinstance(spot_taken, Queen) and best_move <= 5:
                    move_data = (piece, move, cords)
                    best_move = moves["QUEEN"]
                # move will take bishop
                elif isinstance(spot_taken, Bishop) and best_move <= 4:
                    move_data = (piece, move, cords)
                    best_move = moves["BISHOP"]
                # move will take knight
                elif isinstance(spot_taken, Knight) and best_move <= 3:
                    move_data = (piece, move, cords)
                    best_move = moves["KNIGHT"]
                # move will take rook
                elif isinstance(spot_taken, Rook) and best_move <= 2:
                    move_data = (piece, move, cords)
                    best_move = moves["ROOK"]
                # move will take pawn
                elif isinstance(spot_taken, Pawn) and best_move <= 1:
                    move_data = (piece, move, cords)
                    best_move = moves["PAWN"]
        if not move_data:
            locations = self.get_piece_locations(Color.BLACK)
            cords = random.choice(locations)
            piece = self.get(cords[0], cords[1])
            moves = piece.valid_moves(cords[0], cords[1])
            while not moves:
                cords = random.choice(locations)
                piece = self.get(cords[0], cords[1])
                moves = piece.valid_moves(cords[0], cords[1])
            move_data = (piece, random.choice(moves), cords)
        self.move(move_data[0], move_data[2][0], move_data[2][1], move_data[1][0], move_data[1][1])
        if self.current_player == Color.BLACK:
            self.switch_player()
        return f"BLACK moved {move_data[0].__class__.__name__}\n"


    class BoardStack:
        """
        a board stack is needed for the undo method to hold all of the data of previous moves and states of the baord
        in case the player wants to go back on a move they made previously.
        """
        def __init__(self) -> None:
            self._data: list[list] = []

        def length(self) -> int:
            return len(self._data)

        def peek(self) -> list[list]:
            if not self._data:
                raise ValueError("Cannot peek from an empty stack")
            return self._data[-1]

        def pop(self) -> list[list]:
            if not self._data:
                raise ValueError("Cannot pop from an empty stack")
            data = self.peek()
            del self._data[-1]
            return data

        def push(self, board: list[list]) -> None:
            self._data.append(board)


def __main__():
    g = Game()


if __name__ == '__main__':
    __main__()