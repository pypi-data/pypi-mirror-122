# Py2048-Engine
A pure 🐍 , fully type hinted, well documented 2048 Engine.

## Installation

First, install `Py2048-Engine`.

The easiest method is with PyPi:
`$ pip install Py2048-Engine`

Alternatively, you can clone the repo:
`$ git clone https://github.com/http-samc/2048.py`

## Getting Started

### If you're looking to play the game itself...
You can get a quick and intuivite introduction to the engine by using the built-in game tester. First import `runTest()` from the package and call it to get started.
```Python
>>> from Py2048_Engine.Test import runTest
>>> runTest()
```

You'll be given a printout of the board, a 4 by 4 grid. All 'empty' spaces have a `-`. From here, you are in a loop of being able to move in any direction.
```
-       -       -       4
-       -       -       -
-       -       2       -
-       -       -       -

Choose a movement:
        [1] Left
        [2] Right
        [3] Up
        [4] Down

Choice: 1
```
*Many moves later...*
```
32      -       -       -
-       -       4       -
2       -       -       -
4       -       -       -
```

Eventually, you'll get a printout when you win or lose.


### If you want to implement the engine in a project...

First, import the game class from `Py2048_Engine.Game`. Then, you can create a game like:

```Python
from Py2048_Engine.Game import Game

game = Game()
```

You can get your current board via `Game.__repr__()` (pretty printed String) or access the raw board (2D int array) with `Game.getBoard()` like:

```Python
print(game) # Pretty printed output
board = game.getBoard() # Type: List[List[int]], better for custom applications
```

You can perform an action on your game board by using `Game.left()`, `Game.right()`, `Game.up()`, or `Game.down()`.

```Python
game.left()
game.right()
game.up()
game.down()
```

Eventually, you'll either win or lose. To handle this, you want to catch some `Exceptions` from `Py2048_Engine.Exceptions`.

All thrown `Exceptions` inherit from `Py2048_Engine.Exceptions.GameException`, with `Py2048_Engine.Exceptions.GameWonException` signifing a game win and `Py2048_Engine.Exceptions.GameLostException` signifing a game loss.

`GameException` and its children have a few important attributes, especially if you're prototyping.

| Attribute | Desc |
| --- | --- |
| `message` | a message describing why the `GameException` was thrown. |
| `numMoves` | the number of moves taken before the `GameException` was thrown. |
| `board` | the final board before the `GameException` was thrown. Type of `List[List[int]]` |

A sample catch might look like this:
```Python
...

from Py2048_Engine.Exceptions import GameException, GameWonException, GameLostException

while True:

    try:
        game.left()
        game.right()
        game.up()
        game.down()

    except GameException as e:
        # At this point we have access to the final board,
        # final number of moves, and an exit message.

        if type(e) is GameWonException:
            print("YOU WON!!!")
        
        elif type(e) is GameLostException:
            print("Better luck next time :(")
        
        print(e.message)
        print(f"Finished in {e.numMoves} moves.")
        print(f"Final board:\n{e.finalBoard}")
```

## Questions?
See the full docs at [DOCS.md](https://github.com/http-samc/2048.py/blob/main/DOCS.md). If you have any other questions, feel free to contact the author, [Samarth Chitgopekar](mailto:sam@chitgopekar.tech)!

## Special Thanks
Thanks to [this](https://stackoverflow.com/questions/13214809/pretty-print-2d-list) post's marked answer on Stack Overflow for some help on `Game.__repr__()` and Bhargavi Goel's 2017 [paper](https://www.ripublication.com/aama17/aamav12n1_01.pdf) on the mathematics behind 2048, which helped me create this engine!