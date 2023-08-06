"""
    Exceptions.py 10/10/2021
    MIT License

    Copyright (c) 2021 http-samc
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from typing import List

class GameException(Exception):
    """Base Exception raised when a key event happens within a Game.
    
    Attrs:
        board (List[List[int]]): the final board before the exception was thrown.
        numMoves (int): the number of moves taken before the exception was thrown.
        message (str): a description of the exception.
    """

    board: List[List[int]]
    numMoves: int
    message: str

    def __init__(self, board: List[List[int]], numMoves: int, message: str) -> None:
        """Base Exception raised when a key event happens within a Game.

        Args:
            board (List[List[int]]): the final board before the exception was thrown.
            numMoves (int): the number of moves taken before the exception was thrown.
            message (str): a description of the exception.
        """

        self.board = board
        self.numMoves = numMoves
        self.message = message
        
        super().__init__(message)

class GameWonException(GameException):
    """Exception raised when user loses a Game.
    
    Inherits: GameException

    Noninherited Attrs: None
    """

    def __init__(self, board: List[List[int]], numMoves: int, message: str = "Game won - a tile with the value 2048 reached!") -> None:
        """Exception raised when a user wins a Game a tile (position in the board) has a value of 2048.

        Args:
            board (List[List[int]]): the final board before the exception was thrown.
            numMoves (int): the number of moves taken before the exception was thrown.
            message (str, optional): a description of the exception. Defaults to "Game won - a tile with the value 2048 reached!".
        """

        super().__init__(board, numMoves, message)

class GameLostException(GameException):
    """Exception raised when user loses a Game.
    
    Inherits: GameException

    Noninherited Attrs: None
    """

    def __init__(self, board: List[List[int]], numMoves: int, message: str = "Game lost - no blank spaces left and no tile combinations left!") -> None:
        """Exception raised when a user loses a Game (no 'None' spaces left and no tiles can be combined)

        Args:
            board (List[List[int]]): the final board before the exception was thrown.
            numMoves (int): the number of moves taken before the exception was thrown.
            message (str, optional): a description of the exception. Defaults to "Game lost - no blank spaces left and no tile combinations left!".
        """
        
        super().__init__(board, numMoves, message)