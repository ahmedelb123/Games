from enums import PlayerNumber, PlayerSign

class Place:
    def __init__(self, number, occupant = None):
        self.occupant = occupant
        self.number = number
    def is_availabality(self):
        return self.occupant == None
    def add_occupant(self, player):
        if self.is_availabality():
            self.occupant = player
        return self.is_availabality()
    
   
class Player:
    def __init__(self, player_number: PlayerNumber , sign: PlayerSign):
        self.player_number = player_number
        self.sign = sign