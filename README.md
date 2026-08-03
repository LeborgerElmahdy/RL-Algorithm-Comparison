# RL Algorithm Test Blueprint

## Goal
They would all be implemented around attack / defend states, with a basic
variable for hp, and it should maximize its own hp while minimizing player
hp. It won't have limited turns — it's a fight till either side is
eliminated.

## Core Variables
- `enemy_hp`, `player_hp` (0–100)
- `base_attack` (10)
- `turn_count` (soft training-only cap, e.g. 200–500 turns, purely a
  training-loop safety valve — not a loss condition, no effect on the fight
  itself, which has no turn limit)

## State Space
- Own HP %
- Player HP %
- Player's previous action
- Turns elapsed

## Action Space
- **Attack** — guaranteed 100% damage, no cost
- **Defend** — mitigates 70% of damage recieved, never fully blocks
- **Dodge-Counter** — 70% chance of success: negate damage and deal 100% damage.
  30% chance: take 150% damage.

## Turn Resolution
Both sides choose their actions at once, the agent reacts to the Player
PREVIOUS state NOT the current State.

## Anti-Stalemate
Chip damage on Defend ensures it won't be stuck in an attack defend attack
defend loop with neither side losing health — every action combination
(Attack/Attack, Attack/Defend, Defend/Defend, any Dodge-Counter outcome)
results in some HP decreasing every turn, since chip damage is never 0.

## Reward Signal
- `+` for damage dealt
- `−` for damage taken
- Small `−` per turn (time penalty)
- Win/loss bonus at episode end

## Episode Structure
- Ends on `HP = 0`
- No fixed max turns in the actual fight
- Soft max-turn cap during training only, as a discard/abort safeguard

## Scripted Player Policy
- **HP-based phases**:
  - HP > 60%: mostly Attack, occasional Dodge-Counter => 70% attack, 30% dodge
  - HP 30–60%: even mix of all three => 40% attack, 30% dodge, 30% defend
  - HP < 30%: mostly Defend, with a chance of Dodge-Counter, 70% defend, 30% dodge
- **Reactive conditioning**:
  - Enemy Attacked twice in a row → player weights Dodge-Counter higher
  - Enemy Defended twice in a row → player weights Attack higher
  - Otherwise → falls back to phase-based weights above
- **Persistent randomness**: cap any single action's probability at 50–70%
  even within a phase/reaction rule

## Evaluation Metrics
- Win rate vs. the scripted player
- Average episode length
- Damage efficiency ratio (damage dealt / damage taken)
- Action diversity (entropy of action distribution)
- Training stability / convergence speed

## Fairness Constraints
Same state/action space, same reward function, same opponent policy, same
episode-length rules for every algorithm tested — only the algorithm
changes.
