from enums import PlayerNumber, PlayerSign
from basic_component import Player
from board import Board

class TicTacToeGame:
    def __init__(self):
        self.game_board = Board()
        self.player_1 = Player(PlayerNumber.FIRST_PLAYER, PlayerSign.X)
        self.player_2 = Player(PlayerNumber.SECOND_PLAYER, PlayerSign.O)

    def play(self, player, place_number):
        place = self.game_board.get_place(place_number)
        if player == PlayerNumber.FIRST_PLAYER.value:
            place.occupant = self.player_1

        else:
            place.occupant = self.player_2

   
    
    def check_win_case(self, player, win_case):
        for place_number in win_case:
            if self.game_board.get_place(place_number).occupant != player:
                return False
        return True
    
    def check_end_game(self, player):
        win_cases = [[0, 1, 2], [3, 4, 5], [6, 7, 8],[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for win_case in win_cases:
            if self.check_win_case(player, win_case):
                return True
        return False
                
    
    

    def check_validatiopn_input(self, place_numb):
        if place_numb.isdigit():
            place = self.game_board.get_place(int(place_numb))
            return int(place_numb) in range(0, 9) and  place.occupant == None
        return False
    