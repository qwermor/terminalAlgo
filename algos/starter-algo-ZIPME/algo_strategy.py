import gamelib
import random
import math
import warnings
from sys import maxsize
attack_stage = 0
lateGame_tunnel = 0

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):

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

    
    def starter_strategy(self, game_state):
        

        self.round1(game_state)

        self.buildBase(game_state)

        self.deploy_attackers(game_state)

        self.build_defences(game_state)

        self.deploy_SCRAMBLER(game_state)


    
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
            firewall_locations = [[ 3, 12],[ 24, 12],[ 5, 11],[ 9, 11],[ 13, 11],[ 14, 11],[ 18, 11],[ 22, 11],[ 25, 12],[ 26, 12]]
            for location in firewall_locations:
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)  

            #filter
            firewall_locations = [[ 3, 13],[ 24, 13],[ 5, 12],[ 9, 12],[ 10, 12],[ 13, 12],[ 14, 12],[ 17, 12],[ 18, 12],[ 22, 12],[ 26, 13],[ 27, 13]]
            for location in firewall_locations:
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)
            

        firewall_locations = [[ 2, 13],[ 4, 12],[ 26, 12],[ 24, 12],[ 25, 12],[ 5, 11],[ 9, 11],[ 13, 11],[ 14, 11],[ 18, 11],[ 22, 11],[ 6, 10],[ 9, 10],[ 18, 10],[ 21, 10],[ 7, 9],[ 20, 9]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location) 





    def build_defences(self, game_state):

 
        #FILTER
        firewall_locations = [[ 4, 13],[ 24, 13],[ 25, 13],[ 5, 12],[ 9, 12],[ 10, 12],[ 17, 12],[ 18, 12],[ 22, 12],[ 23, 12],[ 6, 11],[ 11, 11],[ 12, 11],[ 15, 11],[ 16, 11],[ 21, 11],[ 20, 10],[ 7, 9],[ 8, 8],[ 26, 13],[ 27, 13]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

        ##ENCRYPTOR making room
        if ((game_state.turn_number == 10)):
        	game_state.attempt_remove([ 3, 12]) 
        ##ENCRYPTOR
        if ((game_state.turn_number > 8)):
            firewall_locations = [[ 3, 12],[ 4, 11],[ 5, 10]]
            for location in firewall_locations:
                if game_state.can_spawn(ENCRYPTOR, location):
                    game_state.attempt_spawn(ENCRYPTOR, location)
        ##LATEGAME
        if ((game_state.turn_number > 20)):
            firewall_locations = [[ 3, 13],[ 9, 10],[ 18, 10],[ 26, 13],[ 27, 13],[ 25, 11],[10, 11],[17,11]]
            for location in firewall_locations:
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)

        if (game_state.get_resource(game_state.BITS) > 20):
            firewall_locations = [[ 11, 8],[ 12, 8],[ 15, 8],[ 16, 8],[ 19, 8],[ 9, 7]]
            for location in firewall_locations:
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)
        global lateGame_tunnel
        ##Tunnelstrat          
        if ((game_state.turn_number > 30)):
            firewall_locations = [[ 9, 7],[ 10, 6],[ 11, 5],[ 12, 4],[ 13, 3],[ 14, 2],[ 15, 1]]
            for location in firewall_locations:
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)
                    lateGame_tunnel = 1
                    game_state.attempt_remove([ 1, 13])
                    game_state.attempt_remove([ 0, 13])

    def deploy_SCRAMBLER(self, game_state):
        if (game_state.turn_number <= 9):
            deploy_location = [[ 4, 9],[ 23, 9],[ 10, 3],[ 17, 3]]
            for location in deploy_location:
                if game_state.can_spawn(SCRAMBLER, location):
                    game_state.attempt_spawn(SCRAMBLER, location)




    def deploy_attackers(self, game_state):
        global attack_stage
        global lateGame_tunnel
        free = not(game_state.contains_stationary_unit([ 0, 14]) and (game_state.contains_stationary_unit([ 1, 14]) or game_state.contains_stationary_unit([ 1, 15])))

        if (not free and (attack_stage != 1) and (lateGame_tunnel == 0)): #closing gap
            attack_stage = 0
            for location in [[0,13],[1,13]]:
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)

        if (attack_stage == 1): #attacking emp
            while game_state.can_spawn(EMP, [2, 11]):
                game_state.attempt_spawn(EMP, [2, 11])
            attack_stage = 2

        if (free or (lateGame_tunnel == 1)): #follow up
            while (game_state.get_resource(game_state.BITS) >= 1):
                if (lateGame_tunnel == 1): ## sending troops ahad to self-destruct
                    if (game_state.can_spawn(PING, [ 12, 1])):
                        game_state.attempt_spawn(PING, [ 12, 1])                       
                if (game_state.can_spawn(PING, [ 14, 0])):
                    game_state.attempt_spawn(PING, [ 14, 0])

        if (game_state.turn_number <= 10 or game_state.get_resource(game_state.BITS) < 9 + (int (game_state.turn_number / 10) * 3)):
            return
        attack_stage = 1
        game_state.attempt_remove([ 1, 13])
        game_state.attempt_remove([ 0, 13])

        

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
