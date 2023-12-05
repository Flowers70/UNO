import random
import arcade
import arcade.gui
import Constants as C
import Uno_Card
import Pile_Actions
import GameOver


class MyGameView(Pile_Actions.PileActions):
    """ Main application class. """

    def __init__(self):

        Pile_Actions.PileActions.__init__(self)

        self.background = None

    def setup(self):
        # view = MyGameView()
        self.window.show_view(self)
        """ Set up the game here. Call this function to restart the game. """
        # background image
        self.background = arcade.load_texture("venv/Lib/Uno_cards/background_pic.png")
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(C.MAT_WIDTH, C.MAT_HEIGHT, arcade.csscolor.BLACK)
        # pile.position = C.START_X, C.BOTTOM_Y # MIDDLE USED TO BE BOTTOM
        pile.position = C.START_X + 4 * C.X_SPACING, C.MIDDLE_Y
        self.pile_mat_list.append(pile)

        # Create seven piles for a player (Bottom)
        for i in range(7):
            pile = arcade.SpriteSolidColor(C.MAT_WIDTH, C.MAT_HEIGHT, arcade.csscolor.BLACK)
            pile.position = C.START_X + i * C.X_SPACING, C.BOTTOM_Y
            self.pile_mat_list.append(pile)

        # Seven piles for CPU (Top)
        for i in range(7):
            pile = arcade.SpriteSolidColor(C.MAT_WIDTH, C.MAT_HEIGHT, arcade.csscolor.BLACK)
            pile.position = C.START_X + i * C.X_SPACING, C.TOP_Y
            self.pile_mat_list.append(pile)

        # Create the discard pile
        for i in range(1):
            pile = arcade.SpriteSolidColor(C.MAT_WIDTH, C.MAT_HEIGHT, arcade.csscolor.BLACK)
            pile.position = C.START_X + 3 * C.X_SPACING, C.MIDDLE_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        Uno_Card.create_every_card(self.card_list)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(C.PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[C.BOTTOM_FACE_DOWN_PILE].append(card)
            # self.deck.add_card(card)

        # - Pull from that pile into the bottom piles, all face-down
        # Loop for each pile
        for pile_no in range(C.PLAY_PILE_1, C.PLAY_PILE_7 + 1):
            # Deal proper number of cards for that pile
            # for j in range(pile_no - PLAY_PILE_1 + 1):
            # Pop the card off the deck we are dealing from
            card = self.piles[C.BOTTOM_FACE_DOWN_PILE].pop()
            # self.deck.remove_card(card)
            # Put in the proper pile
            self.piles[pile_no].append(card)
            # Put in player's hand
            self.player_hand.add_card(card)
            # Move card to same position as pile we just put it in
            card.position = self.pile_mat_list[pile_no].position
            # Put on top in draw order
            self.pull_to_top(card)

        # Flip up the top cards
        for i in range(C.PLAY_PILE_1, C.PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()

        # Beginning face up card to play off of
        card = self.piles[C.BOTTOM_FACE_DOWN_PILE].pop()
        # self.deck.remove_card(card)

        self.piles[C.DISCARD_PILE].append(card)
        card.position = self.pile_mat_list[C.DISCARD_PILE].position
        # print("Discard Pile Card:", self.piles[C.DISCARD_PILE][-1])
        # print("Cards on discard pile:", len(self.piles[C.DISCARD_PILE]))

        self.pull_to_top(card)

        self.piles[C.DISCARD_PILE][-1].face_up()

        for pile_no in range(C.TOP_PILE_1, C.TOP_PILE_7 + 1):
            # Deal proper number of cards for that pile
            # for j in range(pile_no - PLAY_PILE_1 + 1):
            # Pop the card off the deck we are dealing from
            card = self.piles[C.BOTTOM_FACE_DOWN_PILE].pop()
            # self.deck.remove_card(card)
            # Put in the proper pile
            self.piles[pile_no].append(card)
            # Put in CPU's hand
            # print("Add card to cpu hand:", card.colors, card.type, card.points)
            self.cpu_hand.add_card(card)
            # Move card to same position as pile we just put it in
            card.position = self.pile_mat_list[pile_no].position
            # Put on top in draw order
            self.pull_to_top(card)



    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
                                            self.background)
        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

def main():
    """ Main function """
    # window = MyGame()
    # window.setup()
    # arcade.run()

    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    start_view = MyGameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
