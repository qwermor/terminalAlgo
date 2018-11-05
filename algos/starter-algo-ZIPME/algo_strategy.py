import gamelib
import random
import math
import warnings
from sys import maxsize
#turn_2 = 0
fist = 0

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):

        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))

        self.starter_strategy(game_state)

        game_state.submit_turn()

    def starter_strategy(self, game_state):

        self.row1(game_state)

        self.middle(game_state)

        if game_state.turn_number >= 20:
            self.scraper(game_state)
        global fist            
        if game_state.turn_number >= 30 and fist >= 4:
            self.break_through(game_state)
        else:
            self.attack(game_state)







    def row1(self, game_state):
        firewall_locations = [[ 3, 11],[ 5, 11],[ 8, 11],[ 12, 11],[ 15, 11],[ 19, 11],[ 22, 11],[ 24, 11]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
        
        firewall_locations = [[ 0, 13],[ 27, 13],[ 1, 12],[ 26, 12],[2, 11],[25, 11], [23, 11], [21, 11], [20, 11], [18, 11], [17, 11], [16, 11], [14, 11], [13, 11], [11, 11], [10, 11], [9, 11], [7, 11], [6, 11], [ 3, 10],[ 4, 9],[ 5, 9],[ 6, 9],[ 7, 9],[ 8, 9]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

    def middle(self, game_state):
        firewall_locations = [[ 2, 12],[ 25, 12]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        firewall_locations = [[ 1, 13],[ 2, 13],[ 25, 13],[ 26, 13], [ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 11, 13],[ 12, 13],[ 13, 13],[ 14, 13],[ 15, 13],[ 16, 13],[ 17, 13],[ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)       

        firewall_locations = [[ 23, 9],[ 22, 9,],[21, 9]]
        for location in firewall_locations:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

    def scraper(self, game_state):
        allPoints = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 11, 13],[ 12, 13],[ 13, 13],[ 14, 13],[ 15, 13],[ 16, 13],[ 17, 13],[ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 25, 13],[ 26, 13],[ 27, 13],[ 1, 12],[ 2, 12],[ 25, 12],[ 26, 12],[ 2, 11],[ 3, 11],[ 5, 11],[ 6, 11],[ 7, 11],[ 8, 11],[ 9, 11],[ 10, 11],[ 11, 11],[ 12, 11],[ 13, 11],[ 14, 11],[ 15, 11],[ 16, 11],[ 17, 11],[ 18, 11],[ 19, 11],[ 20, 11],[ 21, 11],[ 22, 11],[ 23, 11],[ 24, 11],[ 25, 11],[ 3, 10],[ 4, 9],[ 5, 9],[ 6, 9],[ 7, 9],[ 8, 9]]
        for firewall in allPoints:       
            units = game_state.game_map[firewall]  #units is now a list of all units at that location
            if len(units) > 0:    # make sure there are units at that location
                 for unit in units:     # loop through all units at that location
                     stability = unit.stability    # get that units stability
                     if (stability / unit.max_stability < 0.3):
                        game_state.attempt_remove(firewall)


    def attack(self, game_state):
        global fist
        fist += 1
        while (game_state.get_resource(game_state.BITS) >= 3):
            game_state.attempt_spawn(EMP, [24,10])

    def break_through(self, game_state):
        global fist
        if (game_state.get_resource(game_state.BITS) >= 15):
            while game_state.can_spawn(PING, [7, 6]):
                game_state.attempt_spawn(PING, [7, 6])
            fist = 0


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
