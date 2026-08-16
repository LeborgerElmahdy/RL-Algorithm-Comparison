from player_object import PlayerObject
import config as cfg
import numpy as np
import random

class CombatEnv:
    def __init__(self):
        self.player = PlayerObject()
        self.agent = PlayerObject()
        self.reset()

    # this calls the playerObject reset() for both player and agent.
    def reset(self):
        self.player.reset()
        self.agent.reset()
        self.turn_count = 0
        self.done = False
        return self.get_state_vector(for_agent=True)

    # used in the actor, which is yet to be implemented
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
    def _one_hot_action(self, action):
    # slot 0 = "no previous action yet", slots 1-3 = attack/defend/dodge
    
        vec = np.zeros(cfg.NUM_ACTIONS + 1)
        vec[0 if action is None else action + 1] = 1
        return vec
    def get_state_vector(self, for_agent=True):
        
        # last_action fields are always one turn behind because we only set them
        # AFTER resolve_combat runs (see step()), so this naturally satisfies
        # "react to previous state, not current state".
        if for_agent:
            own_hp, opp_hp = self.agent.hp_percentage, self.player.hp_percentage
            opp_last_action = self.player.last_action
        else:
            own_hp, opp_hp = self.player.hp_percentage, self.agent.hp_percentage
            opp_last_action = self.agent.last_action
        turn_frac = min(self.turn_count / cfg.MAX_TURNS_PER_EPISODE, 1.0)
        return np.array(
            [own_hp, opp_hp, *self._one_hot_action(opp_last_action), turn_frac],
            dtype=np.float32,
        )
    # resolves combat actions of both sides in a simulatnious fashion
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
        # Scenario 6: Both Dodge        
        elif agent_action == cfg.ACTION_DEFEND and player_action == cfg.ACTION_DEFEND:
            # without this, D/D loops forever at 0 dmg, breaking Anti-Stalemate
            dmg_to_player += cfg.STALEMATE_CHIP_DAMAGE
            dmg_to_agent += cfg.STALEMATE_CHIP_DAMAGE

        return dmg_to_player, dmg_to_agent
    
    def _reward(self, dmg_dealt, dmg_taken ): # agent_died, player_died
        r = cfg.TIME_PENALTY
        r += (dmg_dealt / cfg.ATTACK_DAMAGE) * 1.0
        r += (dmg_taken / cfg.ATTACK_DAMAGE) * cfg.DAMAGE_TAKEN_PENALITY / 10.0
        # this is commented out because we are testing turns not rounds 
        #if agent_died:
        #   r += cfg.DEATH_PENALITY
        #if player_died and not agent_died:
        #    r += cfg.WIN_BONUS
        return r
    
    def step(self, agent_action, player_action):
        dmg_to_player, dmg_to_agent = self.resolve_combat(agent_action, player_action)

        self.player.hp = max(0, self.player.hp - dmg_to_player)
        self.agent.hp = max(0, self.agent.hp - dmg_to_agent)

        # record streaks/last_action AFTER resolving, so next turn's state
        # correctly reflects "previous" action for both sides
        self.player.action_streak.append(player_action)
        self.agent.action_streak.append(agent_action)
        self.player.last_action = player_action
        self.agent.last_action = agent_action

        self.turn_count += 1
        # agent_died = self.agent.hp <= 0
        # player_died = self.player.hp <= 0
        self.done = (self.agent.hp <= 0 or self.player.hp <= 0
                 or self.turn_count >= cfg.MAX_TURNS_PER_EPISODE)

        reward = self._reward(dmg_to_player, dmg_to_agent)
        next_state = self.get_state_vector(for_agent=True)
        return next_state, reward, self.done, {"dmg_to_player": dmg_to_player, "dmg_to_agent": dmg_to_agent}