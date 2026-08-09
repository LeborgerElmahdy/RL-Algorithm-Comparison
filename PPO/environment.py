from player_object import PlayerObject

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
    
    
