import gamelib
import random
import math
import warnings
from sys import maxsize
turns_cd = 2

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
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()
        gamelib.debug_write(len([[ 4, 12],[ 5, 12],[ 6, 12],[ 7, 12],[ 8, 12],[ 9, 12],[ 10, 12],[ 11, 12],[ 12, 12],[ 13, 12],[ 14, 12],[ 15, 12],[ 16, 12],[ 17, 12],[ 18, 12],[ 19, 12],[ 20, 12],[ 21, 12],[ 22, 12],[ 23, 12],[ 24, 12],[ 25, 12],[ 5, 11],[ 6, 11],[ 7, 11],[ 8, 11],[ 9, 11],[ 10, 11],[ 11, 11],[ 12, 11],[ 13, 11],[ 14, 11],[ 15, 11],[ 16, 11],[ 17, 11],[ 18, 11],[ 19, 11],[ 20, 11],[ 21, 11],[ 22, 11],[ 23, 11],[ 24, 11],[ 6, 10],[ 7, 10],[ 8, 10],[ 9, 10],[ 10, 10],[ 11, 10],[ 12, 10],[ 13, 10],[ 14, 10],[ 15, 10],[ 16, 10],[ 17, 10],[ 18, 10],[ 19, 10],[ 20, 10],[ 21, 10],[ 22, 10],[ 23, 10],[ 7, 9],[ 8, 9],[ 9, 9],[ 10, 9],[ 11, 9],[ 12, 9],[ 13, 9],[ 14, 9],[ 15, 9],[ 16, 9],[ 17, 9],[ 18, 9],[ 19, 9],[ 20, 9],[ 21, 9],[ 22, 9],[ 8, 8],[ 9, 8],[ 10, 8],[ 11, 8],[ 12, 8],[ 13, 8],[ 14, 8],[ 15, 8],[ 16, 8],[ 17, 8],[ 18, 8],[ 19, 8],[ 20, 8],[ 21, 8],[ 9, 7],[ 10, 7],[ 11, 7],[ 12, 7],[ 13, 7],[ 14, 7],[ 15, 7],[ 16, 7],[ 17, 7],[ 18, 7],[ 19, 7],[ 20, 7],[ 10, 6],[ 11, 6],[ 12, 6],[ 13, 6],[ 14, 6],[ 15, 6],[ 16, 6],[ 17, 6],[ 18, 6],[ 19, 6],[ 11, 5],[ 12, 5],[ 13, 5],[ 15, 5],[ 16, 5],[ 17, 5],[ 18, 5],[ 12, 4],[ 13, 4],[ 14, 4],[ 15, 4],[ 16, 4],[ 17, 4]]
))


    def starter_strategy(self, game_state):
        if (game_state.turn_number == 0):
            self.early_game(game_state)

        self.build_defences(game_state)

        self.deploy_attackers(game_state)
        global turns_cd
        turns_cd -= 1

    def early_game(self, game_state):
        firewall_locations = [[ 2, 13],[ 27, 13],[ 9, 11],[ 18, 11]] ##[ 26, 12],
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        
        ## tunnel
        firewall_locations = [[ 5, 10],[ 6, 9],[ 7, 8],[ 8, 7],[ 9, 6],[ 10, 5],[ 11, 4],[ 12, 3],[ 13, 2],[ 14, 1], [4,11]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
        
      

    def build_defences(self, game_state):
        #filtertunnel
        firewall_locations = [[ 5, 10],[ 6, 9],[ 7, 8],[ 8, 7],[ 9, 6],[ 10, 5],[ 11, 4],[ 12, 3],[ 13, 2],[ 14, 1]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
        if (game_state.get_resource(game_state.CORES) >= 4):
            if game_state.can_spawn(ENCRYPTOR, [3, 12]):
                game_state.attempt_spawn(ENCRYPTOR, [3, 12])           
        #neccesary
        firewall_locations = [[ 2, 13],[ 3, 13],[ 27, 13],[ 26, 12],[ 9, 11],[ 18, 11],[ 14, 9]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
        ## add filter at [4,11]

        self.randomDES(game_state)

    def randomDES(self, game_state):
        #all spots
        bank = [[ 4, 12],[ 5, 12],[ 6, 12],[ 9, 12],[ 10, 12],[ 13, 12],[ 14, 12],[ 17, 12],[ 18, 12],[ 21, 12],[ 22, 12],[ 23, 12],[ 24, 12],[ 25, 12],[ 5, 11],[ 8, 11],[ 9, 11],[ 10, 11],[ 11, 11],[ 12, 11],[ 13, 11],[ 15, 11],[ 16, 11],[ 17, 11],[ 18, 11],[ 19, 11],[ 20, 11],[ 21, 11],[ 22, 11],[ 23, 11],[ 24, 11],[ 6, 10],[ 7, 10],[ 8, 10],[ 10, 10],[ 11, 10],[ 13, 10],[ 14, 10],[ 15, 10],[ 17, 10],[ 18, 10],[ 19, 10],[ 20, 10],[ 21, 10],[ 22, 10],[ 23, 10],[ 7, 9],[ 9, 9],[ 12, 9],[ 14, 9],[ 16, 9],[ 17, 9],[ 18, 9],[ 19, 9],[ 20, 9],[ 21, 9],[ 22, 9],[ 8, 8],[ 10, 8],[ 13, 8],[ 14, 8],[ 16, 8],[ 17, 8],[ 18, 8],[ 19, 8],[ 20, 8],[ 21, 8],[ 12, 7],[ 14, 7],[ 17, 7],[ 18, 7],[ 19, 7],[ 20, 7],[ 10, 6],[ 14, 6],[ 15, 6],[ 16, 6],[ 17, 6],[ 19, 6],[ 13, 5],[ 15, 5],[ 17, 5],[ 18, 5],[ 16, 4],[ 17, 4]]        
        filtered = [] # filter for free
        gamelib.debug_write("new" + str(len(bank)))
        for location in bank:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        # fill free spots
        while game_state.get_resource(game_state.CORES) >= 3 and len(filtered) > 0:

            location_index = random.randint(0, len(filtered) - 1)
            build_location = filtered[location_index]
            if game_state.can_spawn(DESTRUCTOR, build_location):
                game_state.attempt_spawn(DESTRUCTOR, build_location)
            filtered.remove(build_location)       


    def deploy_attackers(self, game_state):
        global turns_cd
        if (turns_cd == 0):
            while (game_state.get_resource(game_state.BITS) >= 1):
                game_state.attempt_spawn(PING, [13, 0])
                if game_state.can_spawn(PING, [14, 0]):
                    game_state.attempt_spawn(PING, [14, 0])   
            turns_cd = 2            


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
