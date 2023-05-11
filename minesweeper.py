import random
from typing import List


class Board:
    neighbor_of_mines: list[int]

    def __init__(self, board_dimension, number_of_bombs):
        self.grid = None
        self.board_dimension = board_dimension
        self.number_of_bombs = number_of_bombs
        # all the cells of the grid which we have visited
        self.visit = set()
        # in which cell we will place the bombs
        self.bomb_indexes = set()
        self.neighbor_of_mines = []
        self.init_board()

    def init_board(self):
        # create a list with all the indexes of the grid
        indexes = [(i, j) for i in range(self.board_dimension) for j in range(self.board_dimension)]

        # initialize the grid in order all the cells to be unrevealed
        self.grid = []
        for i in range(self.board_dimension):
            self.grid.append([])
            for j in range(self.board_dimension):
                self.grid[i].append(' ')

        # place the bombs in random positions in the grid
        counter = 0
        while counter < self.number_of_bombs:
            bomb_index = random.choice(indexes)
            indexes.remove(bomb_index)
            self.bomb_indexes.add(bomb_index)
            counter += 1

        # initialize a list where we will use it to store the number of neighbor mines each cell has
        for i in range(self.board_dimension):
            self.neighbor_of_mines.append([])
            for _ in range(self.board_dimension):
                self.neighbor_of_mines[i].append(0)

        # calculate the number of mines each cell has
        for i in range(self.board_dimension):
            for j in range(self.board_dimension):
                # if the cell (i,j) is in the set of bombs then increase the neighbor cells by one
                if (i, j) in self.bomb_indexes:
                    if i - 1 >= 0:
                        self.neighbor_of_mines[i - 1][j] += 1
                    if i + 1 < self.board_dimension:
                        self.neighbor_of_mines[i + 1][j] += 1
                    if j - 1 >= 0:
                        self.neighbor_of_mines[i][j - 1] += 1
                    if j + 1 < self.board_dimension:
                        self.neighbor_of_mines[i][j + 1] += 1
                    if i - 1 >= 0 and j - 1 >= 0:
                        self.neighbor_of_mines[i - 1][j - 1] += 1
                    if i - 1 >= 0 and j + 1 < self.board_dimension:
                        self.neighbor_of_mines[i - 1][j + 1] += 1
                    if i + 1 < self.board_dimension and j - 1 >= 0:
                        self.neighbor_of_mines[i + 1][j - 1] += 1
                    if i + 1 < self.board_dimension and j + 1 < self.board_dimension:
                        self.neighbor_of_mines[i + 1][j + 1] += 1

    def draw_board(self):
        result = ' ' * 3
        for i in range(0, 10):
            result += str(i)
            if i < 9:
                result += ' ' * 2
            else:
                result += '\n'
        result += '-' * 34 + '\n'
        for i in range(self.board_dimension):
            result += (str(i) + ' ' + '|')
            for j in range(self.board_dimension):
                if (i, j) in self.bomb_indexes:
                    if (i, j) in self.visit:
                        result += (self.grid[i][j] + ' |')
                    else:
                        result += (' ' * 2 + '|')
                elif self.neighbor_of_mines[i][j] < 10:
                    result += (str(self.grid[i][j]) + ' |')
                else:
                    if (i, j) in self.visit:
                        result += (str(self.grid[i][j]) + '|')
                    else:
                        result += (' ' * 2 + '|')
            result += '\n'
        print(result)


def play(clickX, clickY, board, counter):
    # check if the row,column of the cell is out of bounds
    if clickX < 0 or clickX >= board.board_dimension or clickY < 0 or clickY >= board.board_dimension:
        return
    # check if we have clicked in a bomb index
    if (clickX, clickY) in board.bomb_indexes and counter == 0:
        board.grid[clickX][clickY] = 'X'
        board.visit.add((clickX, clickY))
        return

    # check if we have visited again the cell, or we have visited a bomb during the recursion which is not allowed so
    # we return back
    if ((clickX, clickY) in board.visit) or ((clickX, clickY) in board.bomb_indexes and counter > 0):
        return

    # add the cell (clickX, clickY) in the visited cells
    board.visit.add((clickX, clickY))

    # in th (clickX, clickY) cell assign the number of neighbor bombs we have in it
    board.grid[clickX][clickY] = board.neighbor_of_mines[clickX][clickY]

    if board.neighbor_of_mines[clickX][clickY] > 0:
        return

    # visit all the neighbor cells
    play(clickX - 1, clickY, board, counter + 1)
    play(clickX + 1, clickY, board, counter + 1)
    play(clickX, clickY - 1, board, counter + 1)
    play(clickX, clickY + 1, board, counter + 1)
    play(clickX + 1, clickY + 1, board, counter + 1)
    play(clickX + 1, clickY - 1, board, counter + 1)
    play(clickX - 1, clickY + 1, board, counter + 1)
    play(clickX - 1, clickY - 1, board, counter + 1)


def main():
    # declare the board and initialize it with the bombs that surround it
    winGame = True
    board = Board(10, 10)

    # free cells of the game.
    free_cells = board.board_dimension ** 2
    while free_cells > board.number_of_bombs:
        board.draw_board()
        while True:
            # Choose one of the free cells of the game
            clickX = int(input("Choose the row of the cell: "))
            clickY = int(input("Choose the column of the cell: "))
            if 0 <= clickX < board.board_dimension and 0 <= clickY < board.board_dimension and (
                    clickX, clickY) not in board.visit:
                break

        play(clickX, clickY, board, 0)
        # free cells that have left in the grid
        free_cells = board.board_dimension ** 2 - len(board.visit)

        # if we have hit in a bomb we lose
        if board.grid[clickX][clickY] == 'X':
            board.draw_board()
            print("You lost!Try again.")
            winGame = False
            break

    if winGame:
        print("Congratulations you won!")


main()
