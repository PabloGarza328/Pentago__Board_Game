# Author: Pablo Garza
# GitHub username: PabloGarza328
# Date: 7/31/24
# Description: Program based on the Pentago game. Allows players to submit moves including rotation of the board,
# checks if the moves are valid, and when necessary,
# updates the state of the game to either a DRAW, BLACK_WON or WHITE_WON.

class Pentago:
    """ Main class of the program. It initializes the board, and contains the make_move method that allows players
    to make moves on the board. It communicates with CheckIfWinner class to aid it in finding out if
    someone has won the game whenever a player adds a ball and after the board rotation is applied"""
    def __init__(self):
        self._Game_State = "UNFINISHED"
        self._matrix = None
        self.initialize()
        self._turn = "black"

    def initialize(self):
        """ Initialize matrix made with a dictionary of lists. Thematrix is filled with #"""
        mat = {}
        for letter in "abcdef":
            mat[letter] = ["#", "#", "#", "#", "#", "#"]
        self._matrix = mat

    def get_game_state(self):
        """Get method that returns the current state of the game"""
        return self._Game_State

    def is_board_full(self):
        """Checks if board is full. If it is, it returns True, else it returns False """
        for row in self._matrix:
            for column in self._matrix[row]:
                if column == "#":
                    return False
        return True

    def check_if_winner(self):
        """Checks if someone has won by making a CheckIfWinner object and calling the winner method.
        If someone has won it returns the color that they are playing with, else it returns none"""
        check = CheckIfWinner(self._matrix)
        winner = check.winner()
        return winner

    def change_matrix_to_integers_1(self):
        """Takes a matrix made with dictionary of lists and return a matrix made with list of lists,
        that ranges from [0][0] through to [5][5]"""
        matrix_list_1 = [0, 1, 2, 3, 4, 5]

        for index, key in enumerate(self._matrix):
            temp_list =[]
            for i in range(6):
                temp_list += [(self._matrix[key][i])]
            matrix_list_1[index] = temp_list
        return matrix_list_1

    def change_integers_to_dictionary(self, matrix):
        """Takes a matrix that is made with a list of lists and returns a matrix made with a dictionary of lists."""
        vertical = 0
        returning_dict = {}
        for letter in "abcdef":
            returning_dict[letter] = [i for i in matrix[vertical]]
            vertical += 1
        return returning_dict

    def apply_rotation(self, rotation, sub_board):
        """Allows the rotation of a sub_board in either clock-wise or anti-clock-wise direction
        Sub_Board and rotation parameters indicate which sub_board and in what direction the rotation will be executed
        It returns the modified board.
        """

        integer_matrix = self.change_matrix_to_integers_1()
        copied_matrix = [row[:] for row in integer_matrix]
        for x in range(3):
            for y in range(3):
                if sub_board == 1:
                    if rotation == "C":
                        copied_matrix[x][y] = integer_matrix[2-y][x]
                    else:
                        copied_matrix[x][y] = integer_matrix[y][2-x]
                elif sub_board == 2:
                    y += 3
                    if rotation == "C":
                        copied_matrix[x][y] = integer_matrix[5-y][3+x]
                    else:
                        copied_matrix[x][y] = integer_matrix[-3+y][5-x]

                elif sub_board == 3:
                    if x in {0, 1, 2}:
                        x += 3
                    if rotation == "C":
                        copied_matrix[x][y] = integer_matrix[5-y][-3+x]
                    else:
                        copied_matrix[x][y] = integer_matrix[3+y][5-x]
                else:
                    if x in {0, 1, 2}:
                        x += 3
                    y += 3
                    if rotation == "C":
                        copied_matrix[x][y] = integer_matrix[8-y][x]
                    else:
                        copied_matrix[x][y] = integer_matrix[y][8-x]

        dictionary_rotated_matrix = self.change_integers_to_dictionary(copied_matrix)  #  Convert matrix back to dictionary of lists form
        return dictionary_rotated_matrix

    def make_move(self, color, position, sub_board, rotation):
        """Takes instructions and executes a move on the board.
        Color parameter defines which player is making the move.
        Position parameter indicates where the player is placing their ball
        Sub_Board and rotation parameters indicate which sub_board and in what direction the rotation will be executed
        First is checks if the move is valid:
        1. If the game has already finished it returns "game is finished"
        2. If it's not the player's turn it returns "not this player's turn"
        3. If the position is not empty is returns "position not empty"
        Then it applies the player's move and checks if someone has won.
        If no one has won it applies the rotation of the board, and finally checking once more if someone has won
        or if the game has reached a DRAW.
        At this point the method will return True"""

        # Check if game has finished.
        if self._Game_State != "UNFINISHED":
            return "game is finished"

        # Check if it's the player's turn.
        if color != self._turn:
            return "not this player's turn"

        column, row = (position[0]), int(position[1])

        # Check if position is empty
        if self._matrix[column][row] != "#":
            return "position is not empty"

        # Register move:
        if color == "white":
            self._matrix[column][row] = "0"
        else:
            self._matrix[column][row] = "*"

        #For troubleshooting:
        #print("New move from ",self._turn, "in: ", column,", ", row)
        #self.print_board()  #for troubleshooting
        #print(rotation, " Rotation in sub board", sub_board)

        # Update next turn's color
        if self._turn == "black":
            self._turn = "white"
        else:
            self._turn = "black"

        # Check if player has won
        winner = self.check_if_winner()
        if winner == "white":
            self._Game_State = "WHITE_WON"
            return True
        elif winner == "black":
            self._Game_State = "BLACK_WON"
            return True

        #  Apply rotation
        self._matrix = self.apply_rotation(rotation, sub_board)

        # Check if player has won
        winner = self.check_if_winner()
        if winner == "white":
            self._Game_State = "WHITE_WON"
            return True
        elif winner == "black":
            self._Game_State = "BLACK_WON"
            return True

        # Check if board is full, if so it's a DRAW
        elif self.is_board_full():
            self._Game_State = "DRAW"


        #self.print_board()  ## for troubleshoot
        return True

    def print_board(self):
        """Allows printing of the board"""
        for key in self._matrix:
            print(self._matrix[key])


class CheckIfWinner:
    """Class that takes in a matrix as a data member, and can check if someone has won the game"""
    def __init__(self, matrix):
        self._matrix = matrix

    def winner(self):
        """Method that checks if someone has won the game. it iterates through the entire board and at each
        spot checks if there is a vertical, horizontal, or diagonal row of 5 consecutive either black or white balls.
        White balls are represented with 0, black with *. The method calls a different function for each possible direction,
         that is horizontal, vertical, diagonal up, diagonal down
        If white has won it returns "white" and if black has won it returns "black". Else it returns None.
         """

        matrix = self.change_matrix_to_integers()  # Convert the matrix to a list of lists form.

        for vertical in range(6):
            for horizontal in range(6):
                val = matrix[vertical][horizontal]  # Assign current position to val
                if val == "0" or val == "*":

                    # check vertical
                    result = self.recursive_vertical_check(val, horizontal, vertical, matrix)

                    if result is not True:
                        # check horizontal
                        result = self.recursive_horizontal_check(val, horizontal, vertical, matrix)

                    if result is not True:
                        # check diagonal down
                        result = self.recursive_d_down(val, horizontal, vertical, matrix)

                    if result is not True:
                        # check diagonal up
                        result = self.recursive_d_up(val, horizontal, vertical, matrix)

                    if result is True:
                        if val == "0":
                            return "white"
                        else:
                            return "black"

    def recursive_vertical_check(self, starting_val, horizontal, vertical, matrix, count=None):
        """Recursive method that checks if there are 5 consecutive balls of the same color in vertical order.
        Starting Val parameter indicates if the value we are checking is either a white or a black ball.
        Horizontal and Vertical parameters indicate the current position.
        Matriz parameter contains the current matrix of the game.
        Count parameter keeps track of how many times the recursive call has been made.
        If count reaches 4 it means there's 5 consecutive either black or white balls, and thus, the game has ended.
        """

        if count is None:
            count = 0

        # check if we've reached a count of 5
        if count == 4:
            return True

        # check vertical
        if vertical < 5:
            if starting_val == matrix[vertical + 1][horizontal]:
                count += 1
                return self.recursive_vertical_check(starting_val, horizontal, vertical + 1, matrix, count)

        return None

    def recursive_horizontal_check(self, starting_val, horizontal, vertical, matrix, count=None):
        """Recursive method that checks if there are 5 consecutive balls of the same color in horizontal order
        Starting Val parameter indicates if the value we are checking is either a white or a black ball.
        Horizontal and Vertical parameters indicate the current position.
        Matriz parameter contains the current matrix of the game.
        Count parameter keeps track of how many times the recursive call has been made.
        If count reaches 4 it means there's 5 consecutive either black or white balls, and thus, the game has ended.
        """
        if count is None:
            count = 0
        # check if we've reached a count of 5
        if count == 4:
            return True
        # check horizontal, from left to right
        if horizontal > 0:
            if starting_val == matrix[vertical][horizontal-1]:
                count += 1
                return self.recursive_horizontal_check(starting_val, horizontal-1, vertical, matrix, count)

        return None

    def recursive_d_down(self,  starting_val, horizontal, vertical, matrix, count=None):
        """Recursive method that checks if there are 5 consecutive balls of the same color in diagonal order with a
        negative slope
        Starting Val parameter indicates if the value we are checking is either a white or a black ball.
        Horizontal and Vertical parameters indicate the current position.
        Matriz parameter contains the current matrix of the game.
        Count parameter keeps track of how many times the recursive call has been made.
        If count reaches 4 it means there's 5 consecutive either black or white balls, and thus, the game has ended.
        """
        if count is None:
            count = 0

        # check if we've reached a count of 5
        if count == 4:
            return True

        if vertical < 5 and horizontal < 5:
            if starting_val == matrix[vertical+1][horizontal+1]:
                count +=1
                return self.recursive_d_down(starting_val, horizontal+1, vertical+1, matrix, count)

        return None

    def recursive_d_up(self, starting_val, horizontal, vertical, matrix, count=None):
        """Recursive method that checks if there are 5 consecutive balls of the same color in diagonal order with a
        positive slope
        Starting Val parameter indicates if the value we are checking is either a white or a black ball.
        Horizontal and Vertical parameters indicate the current position.
        Matriz parameter contains the current matrix of the game.
        Count parameter keeps track of how many times the recursive call has been made.
        If count reaches 4 it means there's 5 consecutive either black or white balls, and thus, the game has ended.
        """
        if count is None:
            count = 0

        # check if we've reached a count of 5
        if count == 4:
            return True

        if 0 < vertical and horizontal < 5:
            if starting_val == matrix[vertical - 1][horizontal + 1]:
                count += 1
                return self.recursive_d_up(starting_val, horizontal + 1, vertical - 1, matrix, count)

        return None

    def change_matrix_to_integers(self):
        """Changes the self._matrix data member, which is a dictionary of lists, and return a matrix
        made with list of lists, that ranges from [0],[0] through to [5],[5]"""
        matrix_list = [0, 1, 2, 3, 4, 5]

        for index, key in enumerate(self._matrix):
            temp_list =[]
            for i in range(6):
                temp_list += [(self._matrix[key][i])]
            matrix_list[index] = temp_list
        return matrix_list

                                 #         [-3+y] [8-x]
        # copied_matrix[3][3] = self._matrix[3][5]
        # copied_matrix[3][4] = self._matrix[4][5]
        # copied_matrix[3][5] = self._matrix[5][5]
        # copied_matrix[4][3] = self._matrix[3][4]
        # copied_matrix[4][4] = self._matrix[4][4]
        # copied_matrix[4][5] = self._matrix[5][4]
        # copied_matrix[2][0] = self._matrix[0][0]
        # copied_matrix[5][1] = self._matrix[4][2]
        # copied_matrix[5][2] = self._matrix[3][2]





# game = Pentago()
#
# print((game.make_move("black", "a3", 2, "A")))
# #game.print_board()
# print((game.make_move("white", "a1", 1, "A")))
# #game.print_board()
# print(game.make_move("black", "d2", 2, "C"))
# #game.print_board()
# print(game.make_move("white", "d3", 3, "C"))
# print(game.make_move("black", "f4", 4, "C"))
# print(game.make_move("white", "e5", 4, "A"))
# print(game.make_move("black", "e1", 3, "C"))
# print(game.make_move("white", "d1", 2, "C"))
# print(game.make_move("black", "f1", 2, "C"))
# print(game.make_move("white", "d3", 1, "C"))
# print(game.make_move("black", "a1", 2, "C"))
# print(game.make_move("white", "d2", 1, "A"))
# print(game.make_move("black", "a1", 3, "C"))
# print(game.make_move("white", "a3", 3, "A"))
# print(game.make_move("black", "a0", 2, "C"))
# print(game.make_move("white", "a2", 2, "C"))
# print(game.make_move("black", "b0", 2, "C"))
# print(game.make_move("white", "b1", 2, "A"))
# print(game.make_move("black", "b2", 3, "C"))
# print(game.make_move("white", "c0", 3, "A"))
# print(game.make_move("black", "c2", 3, "A"))
# print(game.make_move("white", "a3", 3, "A"))
# print(game.make_move("black", "a4", 1, "C"))
# print(game.make_move("white", "a5", 1, "C"))
# print(game.make_move("black", "b3", 1, "C"))
# print(game.make_move("white", "b4", 1, "A"))
# print(game.make_move("black", "b5", 1, "C"))
# print(game.make_move("white", "c3", 1, "A"))
# print(game.make_move("black", "c4", 1, "A"))
# print(game.make_move("white", "d1", 1, "A"))
# print(game.make_move("black", "d2", 2, "A"))
# print(game.make_move("white", "f0", 2, "A"))
# print(game.make_move("black", "f1", 2, "C"))
# print(game.make_move("white", "e3", 2, "C"))
# print(game.make_move("black", "d5", 2, "C"))
# print(game.make_move("white", "e5", 2, "C"))
# print(game.make_move("black", "e4", 2, "C"))
# print(game.make_move("white", "f3", 3, "A"))
# print(game.make_move("black", "c5", 3, "A"))
# print(game.make_move("white", "b3", 2, "A"))
# print(game.make_move("black", "f5", 2, "A"))
# print(game.make_move("white", "c4", 2, "A"))
#
# game.print_board()
# print(game.get_game_state())


#print(game.make_move("black", "a2", 3, "A"))
#print(game.make_move("black", "a2", 3, "A"))



