DQL
PPO
A2C
MADDPG

Base Action Distribution Schema (Starter for the Agent and Permanent for the Player):

HP > 60%: aggressive - 70% attack, 30% dodge
HP 30-60%: balanced - 40% attack, 30% dodge, 30% defend
HP < 30%: defensive - 70% defend, 30% dodge

AGENT GOAL: Minimize PLAYER HP,  Maximize AGENT HP
Both sides choose their actions at once, the agent reacts to the Player's PREVIOUS state, NOT the current State.

Rules:

Both sides have 100hp
Attack does 10 base damage
Defend negates 7 damage

Dodge success rate:70%
Dodge failure rate:30%

Successful doge counter: Deal 100% damage, Take 0% Damage
Failed dodge counter: Deal no damage, Take 150% Damage

Attack vs Attack = both sides take 100% damage (10)
Attack vs Defend = defender takes 30% of the attack damage (3)
Defend vs Defend = no damage taken, Agent gets a penalty for a wasted attack
Attack vs successful dodge = dodger takes no damage, attacker takes 100% damage (10)
Attack vs failed dodge = dodger takes 150% damage (15)
