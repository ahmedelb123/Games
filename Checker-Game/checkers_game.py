from enums import Color
from basic_component import Piece, PiecePlayer, PieceType
from board import Board

class CheckerGame:
    def __init__(self):
        self.board = Board()
        self.make_game_board()

    def check_allow_place(self, place):
        return place.color == Color.WHITE

    def make_game_board(self):
        for row_letter in self.board.rows:
            for column_number in self.board.columns:
                place = self.board.get_place(row_letter + str(column_number))
                if place.name[0] in ['A', 'B', 'C'] and self.check_allow_place(place):
                    place.occupant = Piece(PiecePlayer.FIRST_PLAYER.value, PieceType.NORMAL.value)
                elif place.name[0] in ['F', 'G', 'H'] and self.check_allow_place(place):
                    place.occupant = Piece(PiecePlayer.SECOND_PLAYER.value, PieceType.NORMAL.value)

    def change_places(self, piece, destination):
        piece_place = self.board.get_place(piece)
        destination_place = self.board.get_place(destination)
        destination_place.add_occupant(piece_place.remove_occupant())
        piece_place.remove_occupant()

    def give_interm_piece(self, piece, destination):
        piece_place = self.board.get_place(piece)
        if piece_place.occupant.player == PiecePlayer.FIRST_PLAYER:
            return self.board[self.board.get_index(piece) + 1][int(piece[1]) + ((int(destination[1]) - int(piece[1])) / 2 ) - 1]
        return self.board[self.board.get_index(piece) - 1][int(piece[1]) + ((int(destination[1]) - int(piece[1])) / 2 ) - 1]



    def check_piece_king(self, piece):
        piece_place = self.board.get_place(piece)
        if piece_place.occupant is None:
            return 'There is no piece in this place'
        elif piece_place.occupant.player == PiecePlayer.FIRST_PLAYER.value and piece_place.name[0] == 'H':
            return True
        elif piece_place.occupant.player == PiecePlayer.SECOND_PLAYER.value and piece_place.name[0] == 'A':
            return True

        return False
    
    #This function check the move of the piece and make the changes if the move is correct;
    def check_move_and_change_places_normal_piece(self, piece, destination):
        direction = 1
        if self.board.get_place(destination).occupant != None:
            return False
        if  self.board.get_place(piece).occupant.player == PiecePlayer.SECOND_PLAYER:
            direction = -1
        if self.board.get_index(destination) - self.board.get_index(piece) == direction and abs(int(destination[1]) - int(piece[1])) == 1:
            self.change_places(piece, destination)
            return True
        elif self.board.get_index(destination) - self.board.get_index(piece) == direction * 2 and abs(int(destination[1]) - int(piece[1])) == 2:
            if self.give_interm_piece(piece, destination).occuapnt.player != self.board.get_place(piece).occupant.player:
                self.give_interm_piece(piece, destination).remove_occupant()
                self.change_places()
        return False



    #This function check first if the the path of the king-pice is diagonal or not;
    def make_rules_piece_king(self, piece, destination):
        return int(piece[1]) != int(destination[1]) and abs(self.board.get_index(piece) - self.board.get_index(destination)) == abs(int(piece[1]) - int(destination[1]))


    
    def check_path_piece_king_and_make_changes(self, piece, destination):
        piece_place = self.board.get_place(piece)
        destination_place = self.board.get_place(destination)

        lst1 = list(range(int(piece_place.name[1]), int(destination_place.name[1])))
        lst2 = list(range(self.board.get_index(piece) + 1, self.board.get_index(destination) + 1))
        if self.make_rules_piece_king(piece, destination) and destination_place.occupant == None:
            if int(piece_place.name[1]) > int(destination_place.name[1]):
                lst1 = list(range(int(piece_place.name[1]) - 2, int(destination_place.name[1]) - 2, -1))
            if self.board.get_index(piece) > self.board.get_index(destination):
                lst2 = list(range(self.board.get_index(piece) - 1, self.board.get_index(destination) - 1, -1))
            if destination_place.occupant != None:
                return False

            for row, column in zip(lst2, lst1):
                if self.board.places[row][column] == destination_place and destination_place.occupant == None:
                    self.change_places(piece, destination)
                    return True


                if  self.board.places[row][column].occupant != None:
                    if self.board.places[row][column].occupant.player != piece_place.occupant.player:
                        if self.board.get_index(piece) < self.board.get_index(destination):
                            if int(piece[1]) < int(destination[1]) and self.board.places[row + 1][column + 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                self.change_places(piece, destination)
                                return True

                            elif int(piece[1]) > int(destination[1]) and self.board.places[row + 1][column - 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                self.change_places(piece, destination)
                                return True

                        elif self.board.get_index(piece) > self.board.get_index(destination):
                            if int(piece[1]) < int(destination[1]) and self.board.places[row - 1][column + 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                self.change_places(piece, destination)
                                return True

                            elif int(piece[1]) > int(destination[1]) and self.board.places[row - 1][column - 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                self.change_places(piece, destination)
                                return True
        return False


    def change_pieces_in_board(self, piece, destination):
        piece_place = self.board.get_place(piece)
        if piece_place.occupant.type == PieceType.NORMAL.value:
            return self.check_move_and_change_places_normal_piece(piece, destination)    
        return self.check_path_piece_king_and_make_changes(piece, destination)

    def check_end_game_P1(self):
        for row in self.board.places:
            for place in row:
                if place.occupant != None and place.occupant.player == PiecePlayer.FIRST_PLAYER.value:
                    return False
        return True

    def check_end_game_P2(self):
        for row in self.board.places:
            for place in row:
                if place.occupant != None and place.occupant.player == PiecePlayer.SECOND_PLAYER.value:
                    return False
        return True

    def check_validation_input(self, input1):
        if len(input1) == 2 and input1[1].isdigit() and isinstance(input1[0], str):
            return input1[0].upper() in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] and int(input1[1]) in range(1, 9)
        return False

    def check_validation_player(self, player, piece):
        if self.board.get_place(piece).occupant != None:
            return self.board.get_place(piece).occupant.player == player
        return False