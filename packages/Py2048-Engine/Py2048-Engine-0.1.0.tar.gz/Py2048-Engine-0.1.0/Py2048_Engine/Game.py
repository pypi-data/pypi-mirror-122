"""
    Game.py 10/10/2021
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

"""
    We can represent 2048 as a 2 dimensional array forming a 4 x 4 grid.

    Each 'position' will be an integer value representing the current value
    of the tile. Blank spaces will have a value of None.

    To start, 2 tiles are placed onto the board. For the duration of the game,
    the user can perform 4 actions: 'UP', 'DOWN', 'LEFT', 'RIGHT'.

    Any time the user performs an action, the following processes occur:
        1) All tiles on the grid that have the same value that are 'touching'
        in the direction of motion (Vertical for Up/Down, Horizontal for Left/Right)
        are combined. The resulting tile is placed where the input tile that was the furthest
        'along' the direction of motion was (Highest for Up, Lowest for Down, Leftmost for Left,
        Rightmost for right).
            - If no tiles can be combined AND all spots in the grid are taken (!None) the user LOSES.
            - If any tile has the value of '2048', the user WINS.
        
        2) A tile is generated and added to a spot on the grid
            - The generated tile is either '2' (P = 0.9) or '4' (P = 0.1) 
"""

from random import choices
from typing import List, Tuple

from Py2048_Engine.Exceptions import GameLostException
from Py2048_Engine.Exceptions import GameWonException

class Game:
    """Programatic representation of the game 2048 and its logic
    
    Attrs:
        LEFT (str): Movement constant for the 'left' direction, set as "left".
        RIGHT (str): Movement constant for the 'right' direction, set as "right".
        UP (str): Movement constant for the 'up' direction, set as "up".
        DOWN (str): Movement constant for the 'down' direction, set as "down".

        POPULATION (List[int]): Possible choices for random tile generation.
        WEIGHTS (List[float]): Probabilities for corresponding indicies in Game.POPULATION

        board (List[List[int]]): Game board represented by a 2D array of integers.
        numMoves (int): The amount of moves currently taken. Starts at 0.
        hasOpenSpace (bool): Whether or not the current board has any open spaces.
    """

    POPULATION: List[int] = [2, 4]
    WEIGHTS: List[float] = [0.9, 0.1]

    LEFT: str = "left"
    RIGHT: str = "right"
    UP: str = "up"
    DOWN: str = "down"

    board: List[List[int]] # Game board
    numMoves: int = 0 # Number of moves taken
    hasOpenSpace: bool = True # Whether or not we have an open space, controlled by Game._canContinue()

    """
        Dunder methods
    """

    def __init__(self, startingBoard: List[List[int]] = None) -> None:
        """Generates a 2048 game instance.

        Args:
            startingBoard (List[List[int]], optional): A custom board to start from. Defaults to None (new game).
        """

        if startingBoard:
            self.board = startingBoard
        else:
            self._generateBoard()

    def __repr__(self) -> str:
        """
            Generates a more viewable representation of the current value
            of self.board.

            Equally spaces items in grid, replaces 'None' with '-'.
        """

        # Credit: https://stackoverflow.com/questions/13214809/pretty-print-2d-list

        s: List[List[str]] = [[str(e) if e is not None else "-" for e in row] for row in self.board]
        lens: List[int] = [max(map(len, col)) for col in zip(*s)]
        fmt: str = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table: List[str] = [fmt.format(*row) for row in s]
        
        return '\n'.join(table)

    """
        Private helper methods
    """

    def _getTouchingPositions(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns all positions of 'touching' tiles
        relative to a given position.

        Given position {r, c} with row = r and column = c, touching tiles
        are at (assuming they exist) {r+1, c}, {r-1, c}, {r, c+1}, {r, c-1}.

        This method returns all of the possible positions that exist.

        Args:
            position (Tuple[int]): a position in the format
            (row, col) on self.board.

        Returns:
            List[Tuple[int]]: a list of tuples representing 
            positions in the format (row, col) on self.board.
        """

        row: int
        col: int
        row, col = position

        # Possible positions of touching tiles (not all guarenteed to exist)
        possibleTouchingPositions: List[Tuple[int, int]] = [
            (row+1, col),
            (row-1, col),
            (row, col+1),
            (row, col-1)
        ]

        touchingPositions: List[Tuple[int, int]] = []

        # Find out applicable touching positions
        for row, col in possibleTouchingPositions:
            if row >= 0 and row < 4 and col >= 0 and col < 4:
                touchingPositions.append((row, col))
        
        return touchingPositions

    def _canContinue(self) -> None:
        """
            Always Ran before Game._placeRandomTile() (except for during board initialization).
            
            Throws GameWonException() if a tile on self.board has a value of '2048'.
            Throws GameLostException() IFF both of the following are met:
                1) all tiles are filled (no values on self.board are 'None')
                2) no tiles of the same value 'touch'
                    2.i) given position {r, c} with row = r and column = c, touching tiles
                    are at (assuming they exist) {r+1, c}, {r-1, c}, {r, c+1}, {r, c-1}
            
            Returns: None
        """

        # Check for blank tiles and Game Win

        # We use a bool here instead of an instant return since we want to check for a Game Win
        # which requires iteration through the whole board
        hasBlankTile: bool = False

        for row, _ in enumerate(self.board):
            for col, val in enumerate(_):

                if val is None:
                    hasBlankTile = True # Game can continue (no loss at the moment)
                    continue

                elif val == 2048:
                    raise GameWonException(self.board, self.numMoves) # Handle Game Win
        
        if hasBlankTile:
            self.hasOpenSpace = True # update instance-level tracker
            return # Handle known playable game (>= 1 empty space)
        
        self.hasOpenSpace = False # update instance-level tracker

        # If we have no empty tiles we need to check for touching tiles to confirm playability

        for row, _ in enumerate(self.board):
            for col, val in enumerate(_):

                touchingPositions: List[Tuple[int, int]] = self._getTouchingPositions((row, col))

                # Check if any of the other touching positions match current value
                for row, col in touchingPositions:
                    if val == self.board[row][col]:
                        return # If the user has at least one potential move, we can continue
        
        # If we've made it this far without a return, both conditions for game loss
        # (no empty tiles & no possible moves) have been met and we need to raise GameLostException
        raise GameLostException(self.board, self.numMoves)

    def _placeRandomTile(self) -> None:
        """
            Places a random tile onto self.board with values of either
            '2' (P = 0.9) or '4' (P = 0.1) (defined in class instance vars).

            Returns: None
        """

        # Credit: https://www.ripublication.com/aama17/aamav12n1_01.pdf for probability distributions
        
        # Because of preprocessing done by Game._canContinue(), we
        # are guarenteed >= 1 blankTilePosition if this method runs
        # b/c it is only called if self.hasOpenSpace

        blankTilePositions: List[Tuple[int]] = []

        for row, _ in enumerate(self.board):
            for col, _ in enumerate(self.board):

                if self.board[row][col] is None:
                    blankTilePositions.append((row, col))
        
        # Getitng random tile's value and position
        tileRow: int
        tileCol: int

        tileRow, tileCol = choices(blankTilePositions)[0]
        tileValue: int = choices(Game.POPULATION, Game.WEIGHTS)[0]

        # Updating board with random tile
        self.board[tileRow][tileCol] = tileValue

    def _generateBoard(self) -> None:
        """
            Creates a 2 dimensional array of type List[List[int]]
            representing a 2048 gamae board and sets it to self.board.

            All values are initialized to 'None', except for 2 random positions
            being prefilled with values from calls to Game._placeRandomTile().

            Returns: None
        """

        self.board = [ [None] * 4 for _ in range(4) ]
        self._placeRandomTile()
        self._placeRandomTile()

    def _compressArray(self, array: List[int], direction: str) -> List[int]:
        """Compresses an array in a specified direction by pushing all non-None
        values together and either appending or prepending the None values, depending
        on direction. Combines like tiles together.

        Args:
            array (List[int]): the input array.
            direction (str): the direction of compression, represented by the
            class constants: LEFT, RIGHT, UP, DOWN.

        Returns:
            List[int]: the compressed array.
        """
        
        # Temp remove all None values
        filteredArray:  List[int] = [elem for elem in array if not elem is None]

        # Temp reverse to standardize compression direction
        if direction == self.DOWN or direction == self.RIGHT:
            filteredArray = list(reversed(filteredArray))

        # Iterate over filtered array
        for i, val in enumerate(filteredArray):

            # No more comparisons
            if i+1 >= len(filteredArray):
                break
            
            # Our curr elem = our next elem -> we can compress
            if val == filteredArray[i+1]:
                filteredArray[i] = 2*val # Double our current value
                filteredArray.pop(i+1) # Remove our next value
            
        # Reintroduce original compression direction if applicable
        if direction == self.DOWN or direction == self.RIGHT:
            filteredArray = list(reversed(filteredArray))

        # Reintroduce None values
        if direction == self.LEFT or direction == self.UP:
            compressedArray: List[int] = filteredArray
            
            for _ in range(4-len(filteredArray)):
                compressedArray.append(None)

        elif direction == self.RIGHT or direction == self.DOWN:
            compressedArray: List[int] = filteredArray
            
            for _ in range(4-len(filteredArray)):
                compressedArray.insert(0, None)    
                    
        return compressedArray

    def _move(self, direction: str) -> None:
        """Performs a movement in a given direction, if possible.

        Args:
            direction (str): The direction to move, represented by the
            class constants: LEFT, RIGHT, UP, DOWN.
        """

        self._canContinue()
        
        if direction == self.LEFT or direction == self.RIGHT:
            for i, row in enumerate(self.board):
                self.board[i] = self._compressArray(row, direction)

        
        elif direction == self.DOWN or direction == self.UP:
            for col in range(4):
                column: List[int] = []

                for row in range(4):
                    column.append(self.board[row][col])

                newColumn: List[int] = self._compressArray(column, direction)

                for row in range(4):
                    self.board[row][col] = newColumn[row]
        
        if self.hasOpenSpace:
            self._placeRandomTile()
        
        self.numMoves += 1

    """
        Public methods
    """
    
    # Movement methods
    def left(self) -> None:
        """
            Simulates a 'left' arrow key/swipe on the board.

            Can raise a GameWonException or a GameLostException
            if the function call's corresponding movement triggers it.
        """

        self._move(self.LEFT)

    def right(self) -> None:
        """
            Simulates a 'right' key/swipe on the board.

            Can raise a GameWonException or a GameLostException
            if the function call's corresponding movement triggers it.
        """

        self._move(self.RIGHT)

    def up(self) -> None:
        """
            Simulates a 'up' key/swipe on the board.

            Can raise a GameWonException or a GameLostException
            if the function call's corresponding movement triggers it.
        """

        self._move(self.UP)

    def down(self) -> None:
        """
            Simulates a 'down' key/swipe on the board.

            Can raise a GameWonException or a GameLostException
            if the function call's corresponding movement triggers it.
        """

        self._move(self.DOWN)

    # Getters
    def getBoard(self) -> List[List[int]]:
        """Getter for the current game board.

        Returns:
            List[List[int]]: The current game board.
        """

        return self.board
    
    def getNumMoves(self) -> int:
        """Getter for the current number of moves.

        Returns:
            int: The current number of moves.
        """

        return self.numMoves