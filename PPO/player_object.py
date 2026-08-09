import config as cfg
import random

class PlayerObject:
    def __init__(self):
        self.reset()

    #hmmm i wonder what this does!
    def reset(self):
        self.hp = cfg.MAX_HP
        self.last_action = None
        self.action_streak = []
        self.action_weights = []

    #compares current hp with the phase thresholds in the config
    def get_phase(self):
        if self.hp_percentage > cfg.PHASE_HIGH_HP:
            state_phase = "Aggressive"
        elif self.hp_percentage < cfg.PHASE_LOW_HP:
            state_phase = "Defensive"
        else:
            state_phase = "Balanced"

        return state_phase

    #sets the action weights based on current phase
    def set_weights(self):
        self.action_weights = cfg.PHASE_WEIGHTS[self.get_phase().lower()].copy()

    #chooses actions based on weighted probabilities, currntly used in both player and agent. in the future this will be for the player only
    def choose_action_probablistic(self, enemy_action_streak):

        self.set_weights()

        # grabs a list of the enemies past actions starting from the most recent
        streak = enemy_action_streak[-cfg.REACTIVE_STREAK_LENGTH:]

        # checks if the last "streak length" actions have been the same, and triggers a reaction accordingly
        if len(streak) == cfg.REACTIVE_STREAK_LENGTH:
            if all(a == cfg.ACTION_ATTACK for a in streak):
                self.action_weights[cfg.ACTION_DODGE_COUNTER] += cfg.REACTIVE_DODGE_BOOST
            if all(a == cfg.ACTION_DEFEND for a in streak):
                self.action_weights[cfg.ACTION_ATTACK] += cfg.REACTIVE_ATTACK_BOOST

        #normalizes the weights incase anything goes above 100%
        total = sum(self.action_weights)
        self.action_weights = [w / total for w in self.action_weights]

        # does the actual choosing, fire emoji
        return random.choices([cfg.ACTION_ATTACK, cfg.ACTION_DEFEND, cfg.ACTION_DODGE_COUNTER], weights = self.action_weights, k = 1)[0]

    @property
    def hp_percentage(self):
        return max(0.0, self.hp / cfg.MAX_HP)
    #hmmm i wonder what this does!