# --- Core stats ---
MAX_HP = 100

ATTACK_DAMAGE = 10                              # Dealt to attack target
DEFEND_CHIP_DAMAGE_RATIO = 0.3                  # Dealt to defender
DODGE_COUNTER_DAMAGE = ATTACK_DAMAGE * 1.2      # Dealt to attack target
DODGE_COUNTER_FAIL_DAMAGE = ATTACK_DAMAGE * 1.5 # Dealt to attack originator
DODGE_COUNTER_SUCCESS_RATE = 0.7

# --- Penalties ---
TIME_PENALTY = -0.05
DAMAGE_TAKEN_PENALITY = -10
DEATH_PENALITY = -100

# --- Actions ---
ACTION_NAMES = ["Attack", "Defend", "Dodge"]

# --- Actions Indices ---
ACTION_ATTACK = 0
ACTION_DEFEND = 1
ACTION_DODGE_COUNTER = 2

NUM_ACTIONS = 3

# --- Player Phases ---

PHASE_HIGH_HP = 0.6   # above, player is "aggressive"
PHASE_LOW_HP = 0.3    # below, player is "defensive"

PHASE_WEIGHTS = {
#                 [Attack, Defend, Dodge]
    "aggressive": [0.70  , 0.05  , 0.25],
    "balanced":   [0.40  , 0.30  , 0.30],
    "defensive":  [0.15  , 0.60  , 0.25],
}

# --- Reaction Triggers ---
REACTIVE_STREAK_LENGTH = 2        # how many repeated enemy actions trigger a reaction
REACTIVE_DODGE_BOOST = 0.25       # added to Dodge-Counter weight if a dodge reaction is triggered
REACTIVE_ATTACK_BOOST = 0.25      # added to Attack weight if a attack reaction is triggered

# --- Hyperparameters ---
GAMMA = 0.99
GAE_LAMBDA = 0.95
EPSILON = 0.2
LEARNING_RATE = 3e-4
EPOCHS = 5