from basic_component import Place

class Board:
    def  __init__(self):
        self.places = []
        for number in range(0, 9):
            self.places.append(Place(number, occupant= None))

    def get_place(self, place_number):
        return self.places[place_number]
    
    def make_board_elem(self, n1, n2):
        row = []
        for place_numb in range(n1, n2):
            if self.places[place_numb].occupant == None:
                row.append(str(self.places[place_numb].number))
            else:
                row.append(self.places[place_numb].occupant.sign.value)
        
        return row

    def make_board_all_elem(self):
        list_of_element = []
        list_of_element.append(self.make_board_elem(0, 3))
        list_of_element.append(self.make_board_elem(3, 6))
        list_of_element.append(self.make_board_elem(6, 9))

        return list_of_element
    
    def print_board(self):
        board_element = self.make_board_all_elem()
        for row in board_element:
            print(' | '.join(row))
            print('-' * 9)