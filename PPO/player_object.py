import config as cfg
import random

class PlayerObject:
    def __init__(self):
        self.reset()

    def reset(self):
        self.hp = cfg.MAX_HP
        self.last_action = None
        self.action_streak = []
        self.action_weights = []

    def get_phase(self):
        if self.hp_percentage > cfg.PHASE_HIGH_HP:
            state_phase = "Aggressive"
        elif self.hp_percentage < cfg.PHASE_LOW_HP:
            state_phase = "Defensive"
        else:
            state_phase = "Balanced"

        return state_phase

    def set_weights(self):
        self.action_weights = cfg.PHASE_WEIGHTS[self.get_phase().lower()].copy()

    def choose_action_probablistic(self, enemy_action_streak):

        self.set_weights()

        # check enemy last state for possible reactions
        streak = enemy_action_streak[-cfg.REACTIVE_STREAK_LENGTH:]

        if len(streak) == cfg.REACTIVE_STREAK_LENGTH:
            if all(a == cfg.ACTION_ATTACK for a in streak):
                self.action_weights[cfg.ACTION_DODGE_COUNTER] += cfg.REACTIVE_DODGE_BOOST
            if all(a == cfg.ACTION_DEFEND for a in streak):
                self.action_weights[cfg.ACTION_ATTACK] += cfg.REACTIVE_ATTACK_BOOST

        total = sum(self.action_weights)
        self.action_weights = [w / total for w in self.action_weights]

        return random.choices([cfg.ACTION_ATTACK, cfg.ACTION_DEFEND, cfg.ACTION_DODGE_COUNTER], weights = self.action_weights, k = 1)[0]

    @property
    def hp_percentage(self):
        return max(0.0, self.hp / cfg.MAX_HP)