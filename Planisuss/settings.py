"""this module contains the various settings of the world and the creatures"""


# world dimensions
NUMCELLS = 50

# battelfield modifiers
ATTACKER_MODIFIER = 1
DEFENDER_MODIFIER = -1

#max sizes for herd and pride
HERD_MAX_SIZE = 100
PRIDE_MAX_SIZE = 50

# vegetob max cell density
MAX_CELL_DENSITY = 100

# energy discrminators
ENERGY_STAYING_DISCRIMINATOR = 0.7
ENERGY_MOVING_DISCRIMINATOR = 0.7

SPLIT_ENERGY_DISCRIMINATOR = 0.3

HUNT_ENERGY_DISCRIMINATOR = 0.7
GRAZE_ENERGY_DISCRIMINATOR = 0.8

# aging energy modifiers
AGING_ENERGY_MODIFIER = -10

# useful costnats
MAX_LIFESPAN = 100
MAX_ENERGY = 100
INITIAL_ENERGY = 80

# portion of vegetob left alive
VEGETOB_TO_LEAVE = 0.3

# morale modifiers
HUNGER_INTELLIGENT_LOSE = 0.01
HUNGER_SOCIAL_ATTITUDE_LOSE = 0.01

SATIETY_SOCIAL_ATTITUDE_GAIN = 0.01
SATIETY_INTELLIGENT_GAIN = 0.02

# high and low morale thresholds
HIGH_MORALE = 0.9
LOW_MORALE = 0.2
