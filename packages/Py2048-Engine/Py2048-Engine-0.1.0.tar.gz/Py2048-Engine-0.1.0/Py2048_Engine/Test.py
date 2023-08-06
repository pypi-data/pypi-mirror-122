"""
    Test.py 10/10/2021
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

from Py2048_Engine.Game import Game
from Py2048_Engine.Exceptions import GameLostException
from Py2048_Engine.Exceptions import GameWonException

def runTest():
    """Run a basic CLI test of the Py2048 Engine."""

    game = Game()

    print(game)

    while True:
        
        try:
            choice = int(input("Choose a movement:\n\t[1] Left\n\t[2] Right\n\t[3] Up\n\t[4] Down\n\nChoice: "))

            if choice == 1: game.left()
            elif choice == 2: game.right()
            elif choice == 3: game.up()
            elif choice == 4: game.down()

            print(f"\n\n{game}\n")

        except Exception as e:

            if type(e) is GameLostException:
                print(f"Game lost after {e.numMoves} moves!\nFinal Board:")
                print(e.board)
                break

            elif type(e) is GameWonException:
                print(f"Game lost after {e.numMoves} moves!\nFinal Board:")
                print(e.board)
                break

            else:
                print("Please make sure to enter a valid selection (integer from [1, 4])!")

if __name__ == "__main__":
    runTest()