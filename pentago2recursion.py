
class Pentago:
    def __init__(self):
        self._Game_State = "UNFINISHED"
        self._matrix = None
        self.initialize()
        self._turn = "black"

    def initialize(self):
        """ Initialize matrix filled with #"""
        mat = {}
        for letter in "abcdef":
            mat[letter] = ["#", "#", "#", "#", "#", "#"]
        self._matrix = mat

    def get_game_state(self):
        return self._Game_State

    def set_game_state(self, state):
        self._Game_State=state

    def is_board_full(self):
        """Checks if board is full """
        for row in self._matrix:
            for column in self._matrix[row]:
                if column == "#":
                    return False
        return True

    def check_if_winner(self):
        """Checks if someone has won"""
        check = CheckIfWinner(self._matrix)
        winner = check.winner()
        return winner

    def make_move(self, color, position, sub_board, rotation):

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

        # Change next turn

        # Check if player has won
        winner = self.check_if_winner()
        if winner == "white":
            self._Game_State = "WHITE_WON"
            return True
        elif winner == "black":
            self._Game_State = "BLACK_WON"
            return True

        #  Apply rotation

        # Check if player has won
        winner = self.check_if_winner()
        if winner == "white":
            self._Game_State = "WHITE_WON"
            return True
        elif winner == "black":
            self._Game_State = "BLACK_WON"
            return True

        # check if board is full, if so it's a DRAW
        elif self.is_board_full():
            self._Game_State = "DRAW"

    def print_board(self):
        for key in self._matrix:
            print(self._matrix[key])

class CheckIfWinner():
    def __init__(self, matrix):
        self._matrix = matrix

    def winner(self):

        matrix = self.change_matrix_to_integers()

        for vertical in range(6):
            for horizontal in range(6):
                # get current val
                val = matrix[vertical][horizontal]
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
        """Takes a matrix made with dictionary and return a matrix made with lists of a list,
        that ranges from [0,0] through to [5,5]"""
        matrix_list = [0, 1, 2, 3, 4, 5]

        for index, key in enumerate(self._matrix):
            temp_list =[]
            for i in range(6):
                temp_list += [(self._matrix[key][i])]
            matrix_list[index] = temp_list
        return matrix_list

game = Pentago()

(game.make_move("black", "f0", 2, "cw"))
(game.make_move("black", "e1", 2, "cw"))
(game.make_move("black", "d2", 2, "cw"))
(game.make_move("black", "c3", 2, "cw"))
(game.make_move("black", "b4", 2, "cw"))
print(game.get_game_state())

game.print_board()

