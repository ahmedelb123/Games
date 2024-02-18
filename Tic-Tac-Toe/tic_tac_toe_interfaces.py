from tic_tac_toe_game import TicTacToeGame

class TicTacToeInputInterface:
    def __init__(self):
        self.game = TicTacToeGame()

    def start_game(self):
        self.game.game_board.print_board()
        while True:
            if self.game.check_end_game(self.game.player_2):
                print('Player 2 has won the game')
            while True:
                first_player = input('P1 enter the number of the place where you want to play:')
                if self.game.check_validatiopn_input(first_player) == False:
                    print('This place is not available in the board')
                
                elif self.game.check_validatiopn_input(first_player):
                    self.game.play('P1', int(first_player))
                    break

            self.game.game_board.print_board()

            if self.game.check_end_game(self.game.player_1):
                print('Player 1 has won the game')
            while True:
                second_player = input('P2 enter the number of the place where you want to play:')
                if not self.game.check_validatiopn_input(second_player):
                    print('This place is not available in the board')
                
                elif self.game.check_validatiopn_input(second_player):
                    self.game.play('P2', int(second_player))
                    break

            self.game.game_board.print_board()