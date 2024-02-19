from enums import Color
from basic_component import Place

class Board:
    def __init__(self):
        self.rows = 'ABCDEFGH'
        self.columns = range(1, 9)
        self.places = []
        for row_letter in 'ABCDEFGH':
            row = []
            for column_number in range(1, 9):
                if row_letter in ['A', 'C', 'E', 'G']:
                    if column_number % 2 == 0:
                        row.append(Place(row_letter + str(column_number), Color.BLACK, occupant=None))
                    else:
                        row.append(Place(row_letter + str(column_number), Color.WHITE, occupant=None))

                elif row_letter in ['B', 'D', 'F', 'H']:
                    if column_number % 2 == 0:
                        row.append(Place(row_letter + str(column_number), Color.WHITE, occupant=None))
                    else:
                        row.append(Place(row_letter + str(column_number), Color.BLACK, occupant=None))

            self.places.append(row)

    def print_board(self):
        print('       1        2          3         4          5         6         7         8')

        for row in self.places:
            result = ''
            result += row[0].name[0] + '   '
            for place in row:
                if place.occupant is not None:
                    result += place.occupant.player + '/' + place.occupant.type + ' '
                elif place.color == Color.BLACK:

                    result += 'xxxxxxxxx' + ' '
                else:
                    result += '---------' + ' '
            print(result)

    def get_index(self, place_name):
        used_alphabet = 'ABCDEFGH'
        return used_alphabet.index(place_name[0].upper())
    
    def get_place(self, place_name):
        return self.places[self.get_index(place_name[0])][int(place_name[1]) - 1]