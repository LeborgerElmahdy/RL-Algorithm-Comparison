import random
import config as cnfg

class CombatEnv:
    def __init__(self):

        self.enemy_hp = cnfg.MAX_HP
        self.player_hp = cnfg.MAX_HP
        self.turn_count = 0
 
        self.player_last_action = None
        self.enemy_last_action = None
        self.enemy_action_streak = [] #Tracks if attacks are spammed for reaction triggers
 
        self.done = False

    def reset(self):

        self.enemy_hp = cnfg.MAX_HP
        self.player_hp = cnfg.MAX_HP
        self.turn_count = 0
        self.player_last_action = None
        self.enemy_last_action = None
        self.enemy_action_streak = []
        self.done = False
        return self.get_state()

    def get_state(self):

        return {
            "enemy_hp_percentage": self.enemy_hp / cnfg.MAX_HP,
            "player_hp_percentage": self.player_hp / cnfg.MAX_HP,
            "player_last_action": self.player_last_action,
            "turn_count": self.turn_count,
        }

    def _choose_player_action(self):
        hp_percentage = self.player_hp / cnfg.MAX_HP

        if(hp_percentage > cnfg.PHASE_HIGH_HP):
            weights = list(cnfg.PHASE_WEIGHTS["aggressive"])
        elif(hp_percentage < cnfg.PHASE_LOW_HP):
            weights = list(cnfg.PHASE_WEIGHTS["defensive"])
        else:
            weights = list(cnfg.PHASE_WEIGHTS["balanced"])

        # check enemy last state for possible reactions
        streak = self.enemy_action_streak[-cnfg.REACTIVE_STREAK_LENGTH:]
        if len(streak) == cnfg.REACTIVE_STREAK_LENGTH:
            if all(a == cnfg.ACTION_ATTACK for a in streak):
                weights[cnfg.ACTION_DODGE_COUNTER] += cnfg.REACTIVE_DODGE_BOOST
            if all(a == cnfg.ACTION_DEFEND for a in streak):
                weights[cnfg.ACTION_ATTACK] += cnfg.REACTIVE_ATTACK_BOOST