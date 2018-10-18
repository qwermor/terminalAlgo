import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""

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
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """
    def starter_strategy(self, game_state):

        self.round1(game_state)

        self.buildBase(game_state)


        self.build_defences(game_state)

        self.deploy_SCRAMBLER(game_state)

        self.deploy_attackers(game_state)
    
    def round1(self, game_state):
        if (game_state.turn_number <= 1):
            #filter
            firewall_locations = [[ 24, 13],[ 5, 12],[ 9, 12],[ 13, 12],[ 18, 12],[ 22, 12]]
            for location in firewall_locations:
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)
            
            #Destructors
            firewall_locations = [[ 24, 12],[ 5, 11],[ 9, 11],[ 13, 11],[ 18, 11],[ 22, 11]]
            for location in firewall_locations:
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)


    def buildBase(self, game_state):
        if (game_state.turn_number <= 5):

            #Destructor
            firewall_locations = [[ 3, 12],[ 24, 12],[ 5, 11],[ 9, 11],[ 10, 11],[ 13, 11],[ 14, 11],[ 17, 11],[ 18, 11],[ 22, 11]]
            for location in firewall_locations:
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)  

            #filter
            firewall_locations = [[ 3, 13],[ 24, 13],[ 5, 12],[ 9, 12],[ 10, 12],[ 13, 12],[ 14, 12],[ 17, 12],[ 18, 12],[ 22, 12],[ 26, 13],[ 27, 13]]
            for location in firewall_locations:
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)
            

        firewall_locations = [[ 2, 13],[ 4, 12],[ 24, 12],[ 25, 12],[ 5, 11],[ 9, 11],[ 10, 11],[ 13, 11],[ 14, 11],[ 17, 11],[ 18, 11],[ 22, 11],[ 6, 10],[ 9, 10],[ 18, 10],[ 21, 10],[ 7, 9],[ 20, 9]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location) 





    def build_defences(self, game_state):

 
        #FILTER
        firewall_locations = [[ 4, 13],[ 24, 13],[ 25, 13],[ 5, 12],[ 9, 12],[ 10, 12],[ 17, 12],[ 18, 12],[ 22, 12],[ 23, 12],[ 6, 11],[ 11, 11],[ 12, 11],[ 15, 11],[ 16, 11],[ 21, 11],[ 20, 10],[ 7, 9],[ 8, 8],[ 26, 13],[ 27, 13]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
        #DESTRUCTOR
        firewall_locations = [[ 3, 13],[ 9, 10],[ 18, 10]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
        ##ENCRYPTOR making room
        if ((game_state.turn_number == 10)):
        	game_state.attempt_remove([ 3, 12]) 
        ##ENCRYPTOR
        if ((game_state.turn_number > 8)):
            firewall_locations = [[ 3, 12],[ 4, 11],[ 5, 10]]
            for location in firewall_locations:
                if game_state.can_spawn(ENCRYPTOR, location):
                    game_state.attempt_spawn(ENCRYPTOR, location)

    def deploy_SCRAMBLER(self, game_state):
        if (game_state.turn_number <= 10):
            deploy_location = [[ 2, 11],[ 25, 11],[ 10, 3],[ 17, 3]]
            for location in deploy_location:
                if game_state.can_spawn(SCRAMBLER, location):
                    game_state.attempt_spawn(SCRAMBLER, location)


    def deploy_attackers(self, game_state):
        if (not(game_state.can_spawn(FILTER, [ 14, 1]))):
            while (game_state.get_resource(game_state.BITS) >= 1):
                if (game_state.can_spawn(PING, [ 14, 0])):
                    game_state.attempt_spawn(PING, [ 14, 0])
            game_state.attempt_remove([ 14, 1]) 
        
        if (game_state.turn_number <= 10 or game_state.get_resource(game_state.BITS) < 6 + (int (game_state.turn_number / 10) * 3)):
            return
        while game_state.can_spawn(EMP, [2, 11]):
            game_state.attempt_spawn(EMP, [2, 11])
        game_state.can_spawn(FILTER, [ 14, 1])
        game_state.attempt_spawn(FILTER, [ 14, 1])
        

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
