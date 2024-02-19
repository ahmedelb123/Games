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




    def check_piece_king(self, piece):
        piece_place = self.board.get_place(piece)
        if piece_place.occupant is None:
            return 'There is no piece in this place'
        elif piece_place.occupant.player == PiecePlayer.FIRST_PLAYER.value and piece_place.name[0] == 'H':
            return True
        elif piece_place.occupant.player == PiecePlayer.SECOND_PLAYER.value and piece_place.name[0] == 'A':
            return True

        return False

    def make_rule_piece_norm(self, piece, destination):
        piece_place = self.board.get_place(piece)
        destination_place = self.board.get_place(destination)
        if piece_place.occupant.player == PiecePlayer.FIRST_PLAYER.value:
            if self.board.get_index(destination) == self.board.get_index(piece) + 1 and destination_place.occupant == None:
                if int(piece_place.name[1]) == 1:
                    if int(destination_place.name[1]) == 2:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

                elif int(piece_place.name[1]) == 8:
                    if int(destination_place.name[1]) == 7:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True
                elif int(piece_place.name[1]) > 1 and int(piece_place.name[1]) < 8:
                    if int(destination_place.name[1]) == int(piece_place.name[1]) + 1 or int(destination_place.name[1]) == int(piece_place.name[1]) - 1:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

        if piece_place.occupant.player == PiecePlayer.SECOND_PLAYER.value:
            if self.board.get_index(destination) == self.board.get_index(piece) - 1 and destination_place.occupant == None:
                if int(piece_place.name[1]) == 1:
                    if int(destination_place.name[1]) == 2:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True


                elif int(piece_place.name[1]) == 8:
                    if int(destination_place.name[1]) == 7:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

                elif int(piece_place.name[1]) > 1 and int(piece_place.name[1]) < 8:
                    if int(destination_place.name[1]) == int(piece_place.name[1]) + 1 or int(destination_place.name[1]) == int(piece_place.name[1]) - 1:
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

        if destination_place.occupant == None:
            if int(destination[1]) == int(piece[1]) + 2:
                if piece_place.occupant.player == PiecePlayer.FIRST_PLAYER.value and self.board.places[self.board.get_index(destination) - 1][int(destination[1]) - 2].occupant != None:
                    if self.board.places[self.board.get_index(destination) - 1][int(destination[1]) - 2].occupant.player == PiecePlayer.SECOND_PLAYER.value and self.board.get_index(destination) == self.board.get_index(piece) + 2:
                        self.board.places[self.board.get_index(destination) - 1][int(destination[1]) - 2].remove_occupant()
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

                elif piece_place.occupant.player == PiecePlayer.SECOND_PLAYER.value and self.board.places[self.board.get_index(destination) + 1][int(destination[1]) - 2].occupant != None:
                    if self.board.places[self.board.get_index(destination) + 1][int(destination[1]) - 2].occupant.player == PiecePlayer.FIRST_PLAYER.value and self.board.get_index(destination) == self.board.get_index(piece) - 2:
                        self.board.places[self.board.get_index(destination) + 1][int(destination[1]) - 2].remove_occupant()
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

            elif int(destination[1]) == int(piece_place.name[1]) - 2:

                if piece_place.occupant.player == PiecePlayer.FIRST_PLAYER.value and self.board.places[self.board.get_index(destination) - 1][int(destination[1])].occupant != None:
                    if self.board.places[self.board.get_index(destination) - 1][int(destination[1])].occupant.player == PiecePlayer.SECOND_PLAYER.value and self.board.get_index(destination) == self.board.get_index(piece) + 2:
                        self.board.places[self.board.get_index(destination) - 1][int(destination[1])].remove_occupant()
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True

                elif piece_place.occupant.player == PiecePlayer.SECOND_PLAYER.value and self.board.places[self.board.get_index(destination) + 1][int(destination[1])].occupant != None:
                    if self.board.places[self.board.get_index(destination) + 1][int(destination[1])].occupant.player == PiecePlayer.FIRST_PLAYER.value and self.board.get_index(destination) == self.board.get_index(piece) - 2:
                        self.board.places[self.board.get_index(destination) + 1][int(destination[1])].remove_occupant()
                        destination_place.add_occupant(piece_place.remove_occupant())
                        piece_place.remove_occupant()
                        return True
        return False




    def make_rules_piece_king(self, piece, destination):
        return int(piece[1]) != int(destination[1]) and abs(self.board.get_index(piece) - self.board.get_index(destination)) == abs(int(piece[1]) - int(destination[1]))



    def check_path_piece_king(self, piece, destination):
        piece_place = self.board.get_place(piece)
        destination_place = self.board.get_place(destination)

        lst1 = list(range(int(piece_place.name[1]), int(destination_place.name[1])))
        lst2 = list(range(self.board.get_index(piece) + 1, self.board.get_index(destination) + 1))
        if self.make_rules_piece_king(piece, destination) and destination_place.occupant == None:
            if int(piece_place.name[1]) > int(destination_place.name[1]):
                lst1 = list(range(int(piece_place.name[1]) - 2, int(destination_place.name[1]) - 2, -1))
            if self.board.get_index(piece) > self.board.get_index(destination):
                lst2 = list(range(self.board.get_index(piece) - 1, self.board.get_index(destination) - 1, -1))

            for row, column in zip(lst2, lst1):
                if self.board.places[row][column] == destination_place and destination_place.occupant == None:
                    destination_place.add_occupant(piece_place.remove_occupant())
                    piece_place.remove_occupant()
                    return True


                if  self.board.places[row][column].occupant != None:
                    if self.board.places[row][column].occupant.player == piece_place.occupant.player:
                        return False
                    elif self.board.places[row][column].occupant.player != piece_place.occupant.player:
                        if self.board.get_index(piece) < self.board.get_index(destination):
                            if int(piece[1]) < int(destination[1]) and self.board.places[row + 1][column + 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                destination_place.add_occupant(piece_place.remove_occupant())
                                piece_place.remove_occupant()
                                return True

                            elif int(piece[1]) > int(destination[1]) and self.board.places[row + 1][column - 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                destination_place.add_occupant(piece_place.remove_occupant())
                                piece_place.remove_occupant()
                                return True

                        elif self.board.get_index(piece) > self.board.get_index(destination):
                            if int(piece[1]) < int(destination[1]) and self.board.places[row - 1][column + 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                destination_place.add_occupant(piece_place.remove_occupant())
                                piece_place.remove_occupant()
                                return True

                            elif int(piece[1]) > int(destination[1]) and self.board.places[row - 1][column - 1] == destination_place:
                                self.board.places[row][column].remove_occupant()
                                destination_place.add_occupant(piece_place.remove_occupant())
                                piece_place.remove_occupant()
                                return True
                    return False
        return False


    def change_pieces_in_board(self, piece, destination):
        piece_place = self.board.get_place(piece)
        if piece_place.occupant.type == PieceType.NORMAL.value:
            return self.make_rule_piece_norm(piece, destination)
        else:
            return self.check_path_piece_king(piece, destination)

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