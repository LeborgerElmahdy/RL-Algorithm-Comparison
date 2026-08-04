import random
import config as cfg

class CombatEnv:
    def __init__(self):

        self.enemy_hp = cfg.MAX_HP
        self.player_hp = cfg.MAX_HP
        self.turn_count = 0
 
        self.player_last_action = None
        self.enemy_last_action = None
        self.enemy_action_streak = [] #Tracks if attacks are spammed for reaction triggers
 
        self.done = False

    def reset(self):

        self.enemy_hp = cfg.MAX_HP
        self.player_hp = cfg.MAX_HP
        self.turn_count = 0
        self.player_last_action = None
        self.enemy_last_action = None
        self.enemy_action_streak = []
        self.done = False
        return self.get_state()

    def get_state(self):

        return {
            "enemy_hp_percentage": self.enemy_hp / cfg.MAX_HP,
            "player_hp_percentage": self.player_hp / cfg.MAX_HP,
            "player_last_action": self.player_last_action,
            "turn_count": self.turn_count,
        }

    def _choose_player_action(self):
        hp_percentage = self.player_hp / cfg.MAX_HP

        if(hp_percentage > cfg.PHASE_HIGH_HP):
            weights = list(cfg.PHASE_WEIGHTS["aggressive"])
        elif(hp_percentage < cfg.PHASE_LOW_HP):
            weights = list(cfg.PHASE_WEIGHTS["defensive"])
        else:
            weights = list(cfg.PHASE_WEIGHTS["balanced"])

        # check enemy last state for possible reactions
        streak = self.enemy_action_streak[-cfg.REACTIVE_STREAK_LENGTH:]
        if len(streak) == cfg.REACTIVE_STREAK_LENGTH:
            if all(a == cfg.ACTION_ATTACK for a in streak):
                weights[cfg.ACTION_DODGE_COUNTER] += cfg.REACTIVE_DODGE_BOOST
            if all(a == cfg.ACTION_DEFEND for a in streak):
                weights[cfg.ACTION_ATTACK] += cfg.REACTIVE_ATTACK_BOOST

        total = sum(weights)
        weights = [w / total for w in weights]

        return random.choices([cfg.ACTION_ATTACK, cfg.ACTION_DEFEND, cfg.ACTION_DODGE_COUNTER], weights = weights, k = 1)[0]
    