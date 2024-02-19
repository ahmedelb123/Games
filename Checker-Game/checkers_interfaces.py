from enums import PiecePlayer
from checkers_game import CheckerGame

class InputsInterfaceCheckersGame:
    def __init__(self):
        self.game = CheckerGame()

    def print_instructions(self):
        return ('Hello players \n'
                'This is a checker game, It should be two players for this game \n'
                'This is how the game work  \n'
                'you need to enter the place of  piece that you want to move and the destination of that piece \n'
                'e.g: A1 will be your piece and B2 will be your destination \n'
                'Note: if you dont know the rules of checkers please go learn how the game work and come play with your friend')

    def checker_game(self):
        print(self.print_instructions())
        self.game.board.print_board()
        while True:
            if self.game.check_end_game_P1():
                return 'Congrats player 2 won the game'
            while True:
                x1 = input('P1 Enter the place of the Piece you want to move:')
                y1 = input('P1 Enter the new you place of that piece:')
                if self.game.check_validation_input(x1) == False:
                    print('This place are not available in the board')
                elif self.game.check_validation_input(y1) == False:
                    print('This place are not available in the board')
                elif self.game.check_validation_player(PiecePlayer.FIRST_PLAYER.value, x1) == False:
                    print('Sorry you cant move this piece')
                elif self.game.check_validation_player(PiecePlayer.FIRST_PLAYER.value, x1):
                    the_move = self.game.change_pieces_in_board(x1, y1)
                    if the_move == False:
                        print('You cant do this move')

                    else:
                        print(the_move)
                        break

            if self.game.check_piece_king(y1):
                self.game.board.get_place(y1).occupant.make_king()

            self.game.board.print_board()

            if self.game.check_end_game_P2():
                return 'Congrats player 2 won the game'
            while True:
                x2 = input('P2 Enter the place of the Piece you want to move:')
                y2 = input('P2 Enter the new you place of that piece:')
                if self.game.check_validation_input(x2) == False:
                    print('This place are not available in the board')
                elif self.game.check_validation_input(y2) == False:
                    print('This place are not available in the board')
                elif self.game.check_validation_player(PiecePlayer.SECOND_PLAYER.value, x2) == False:
                    print('Sorry you cant MOVE this piece')
                elif self.game.check_validation_player(PiecePlayer.SECOND_PLAYER.value, x2):
                    the_move = self.game.change_pieces_in_board(x2, y2)
                    if the_move == False:
                        print('You cant do this move')

                    else:
                        print(the_move)
                        break

            if self.game.check_piece_king(y2):
                self.game.board.get_place(y2).occupant.make_king()
            self.game.board.print_board()