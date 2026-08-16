from player_object import PlayerObject
import config as cfg
import random

class CombatEnv:
    def __init__(self):
        self.player = PlayerObject()
        self.agent = PlayerObject()
        self.reset()

    #this calls the playerObject reset() for both player and agent.
    def reset(self):
        self.player.reset()
        self.agent.reset()
        self.turn_count = 0
        self.done = False
        return self.get_state()

    #used in the actor, which is yet to be implemented
    def get_state(self):
        return {
            "player_hp_percentage": self.player.hp_percentage,
            "player_last_action": self.player.last_action,
            "player_phase": self.player.get_phase(),

            "agent_hp_percentage": self.agent.hp_percentage,
            "agent_last_action": self.agent.last_action,
            "agent_phase": self.agent.get_phase(),
            
            "turn_count": self.turn_count,
        }

    #resolves combat actions of both sides in a simulatnious fashion
    def resolve_combat(self, agent_action, player_action):
        dmg_to_player = 0
        dmg_to_agent = 0

        #Scenario 1: Both Attack
        if agent_action == cfg.ACTION_ATTACK and player_action == cfg.ACTION_ATTACK:
            
            dmg_to_player += cfg.ATTACK_DAMAGE
            dmg_to_agent += cfg.ATTACK_DAMAGE

        #Scenario 2: agent Attacks, Player Defends
        elif agent_action == cfg.ACTION_ATTACK and player_action == cfg.ACTION_DEFEND:

            dmg_to_player += cfg.ATTACK_DAMAGE * cfg.DEFEND_CHIP_DAMAGE_RATIO

        #Scenario 3: Player Attacks, agent Defends
        elif player_action == cfg.ACTION_ATTACK and agent_action == cfg.ACTION_DEFEND:

            dmg_to_agent += cfg.ATTACK_DAMAGE * cfg.DEFEND_CHIP_DAMAGE_RATIO

        #Scenario 4: agent Attacks, Player Dodges
        elif agent_action == cfg.ACTION_ATTACK and player_action == cfg.ACTION_DODGE_COUNTER:

            if random.random() < cfg.DODGE_COUNTER_SUCCESS_RATE:
                dmg_to_agent += cfg.DODGE_COUNTER_DAMAGE
            else:
                dmg_to_player += cfg.DODGE_COUNTER_FAIL_DAMAGE

        #Scenario 5: Player Attacks, agent Dodges
        elif player_action == cfg.ACTION_ATTACK and agent_action == cfg.ACTION_DODGE_COUNTER:

            if random.random() < cfg.DODGE_COUNTER_SUCCESS_RATE:
                dmg_to_player += cfg.DODGE_COUNTER_DAMAGE
            else:
                dmg_to_agent += cfg.DODGE_COUNTER_FAIL_DAMAGE

        return dmg_to_player, dmg_to_agent

    def run_epochs(self, epochs, print_data = False):
        #Rudimentary tracking for the amount of ties, wins, and runs.
        Track = {"Tie": 0, "Agent Win": 0, "Player Win": 0, "Total Turns": 0}

        for i in range (epochs):

            Turns = 0
            self.reset()

            while self.player.hp > 0 and self.agent.hp > 0:

                player_action = self.player.choose_action_probablistic(self.agent.action_streak)
                agent_action = self.agent.choose_action_probablistic(self.player.action_streak) #should be changed to use the PPO algorithm later

                player_dmg, agent_dmg = self.resolve_combat(agent_action, player_action)

                self.player.hp -= player_dmg
                self.agent.hp -= agent_dmg

                #Prevents health from going negative for obvious reasons
                self.player.hp = max(0, self.player.hp)
                self.agent.hp = max(0, self.agent.hp)

                if print_data:
                    print(
                        f"[STATUS] >=======<  --- Turn [{Turns + 1}] Summary --- >=======<\n"
                        f"Health   : Player -> {self.player.hp:<10.1f} |  Agent -> {self.agent.hp:.1f}\n"
                        f"Action   : Player -> {cfg.ACTION_NAMES[player_action]:<10} |  Agent -> {cfg.ACTION_NAMES[agent_action]}\n"
                        f"DmgTaken : Player -> {player_dmg:<10.1f} |  Agent -> {agent_dmg:.1f}\n"
                        f"Phase    : Player -> {self.player.get_phase():<10} |  Agent -> {self.agent.get_phase()}\n"
                    )

                Turns += 1

            if(self.player.hp == 0 and self.agent.hp != 0):

                if print_data:
                    print("Agent Wins! \n")

                Track["Agent Win"] += 1

            elif(self.player.hp != 0 and self.agent.hp == 0):

                if print_data:
                    print("Player Wins! \n")

                Track["Player Win"] += 1

            else:

                if print_data:
                    print("Both idiots killed eachother \n")

                Track["Tie"] += 1

            Track["Total Turns"] += Turns
            
        return Track