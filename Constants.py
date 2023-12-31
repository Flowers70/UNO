
# Screen title and size
SCREEN_WIDTH = 850 # was 1024
SCREEN_HEIGHT = 600 # was 768
SCREEN_TITLE = "UNO!"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.1
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = 0.75 * (TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT)

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants (We modified this)
# NEED TO SEPARATE WILDS AND MAYBE ALL COLORS
CARD_COLORS = ["Red", "Blue", "Green", "Yellow"]
CARD_TYPES = [["Wild", "Draw4"], ["Draw2", "Reverse", "Skip"], ["Normal"]]

# If we fan out cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Face down image
# FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"
FACE_DOWN_IMAGE = "venv/Lib/Uno_cards/uno_back.png"

# Constants that represent "what pile is what" for the game
PILE_COUNT = 16  # Changed from 13 -> 16
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
DISCARD_PILE = 15
PLAY_PILE_1 = 1
PLAY_PILE_2 = 2
PLAY_PILE_3 = 3
PLAY_PILE_4 = 4
PLAY_PILE_5 = 5
PLAY_PILE_6 = 6
PLAY_PILE_7 = 7
TOP_PILE_1 = 8
TOP_PILE_2 = 9
TOP_PILE_3 = 10
TOP_PILE_4 = 11
TOP_PILE_5 = 12
TOP_PILE_6 = 13
TOP_PILE_7 = 14
