from typing import Optional

import random
import arcade
import arcade.gui
import Constants as C
import Uno_Card
import Game_Logic


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):

        super().__init__(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        self.background = None

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

        # CPU hand (contains all cards in cpu's hand)
        self.cpu_hand = Uno_Card.Hand()

        # Players' hand (contains all cards in player's hand)
        self.player_hand = Uno_Card.Hand()

        # Deck
        # self.deck = Uno_Card.Hand()

        # Who's turn is it? (Begins with player - not CPU)
        self.player_turn = True

        # # Create UNO! Button
        # self.button = arcade.gui.UIFlatButton("UNO!")

        # Create the buttons
        self.button = arcade.gui.UIFlatButton(800, 450, 200, 10, "UNO!")

    def setup(self):
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
        print("Discard Pile Card:", self.piles[C.DISCARD_PILE][-1])
        print("Cards on discard pile:", len(self.piles[C.DISCARD_PILE]))

        self.pull_to_top(card)

        self.piles[C.DISCARD_PILE][-1].face_up()

        for pile_no in range(C.TOP_PILE_1, C.TOP_PILE_7+1):
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

        # Flip up the top cards
        for i in range(C.TOP_PILE_1, C.TOP_PILE_7 + 1):
            self.piles[i][-1].face_up()


        # cpu_choice = Game_Logic.cpu_select(self.piles[C.DISCARD_PILE][-1], self.cpu_hand, self.deck)
        # print("CPU Chose")
        # print(cpu_choice[0].colors, cpu_choice[0].type, cpu_choice[0].points)
        #
        # for card in cpu_choice[1]:
        #     self.draw_card(False)

        # print()

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

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Uno_Card.Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)

            # Are we clicking on the bottom deck, to flip one card
            if pile_index == C.BOTTOM_FACE_DOWN_PILE:
                # Flip one cards
                self.draw_card(self.player_turn)

            elif primary_card.is_face_down:
                # Is the card face down? In one of those bottom 7 piles? Then flip up
                # if pile_index not in range(C.TOP_PILE_1, C.TOP_PILE_7 + 1):
                #     primary_card.face_up()
                primary_card.face_up()
            elif pile_index != C.DISCARD_PILE:
                # Determine if it is the cpu's turn or the players
                # If it is the player's turn no cards should be moved from the cpu's hand
                if self.player_turn and pile_index not in range(C.TOP_PILE_1, C.TOP_PILE_7+1):
                    # All other cases, grab the face-up card we are clicking on
                    self.held_cards = [primary_card]
                    # Save the position
                    self.held_cards_original_position = [self.held_cards[0].position]
                    # Put on top in drawing order
                    self.pull_to_top(self.held_cards[0])

                    # # Is this a stack of cards? If so, grab the other cards too
                    # card_index = self.piles[pile_index].index(primary_card)
                    # for i in range(card_index + 1, len(self.piles[pile_index])):
                    #     card = self.piles[pile_index][i]
                    #     self.held_cards.append(card)
                    #     self.held_cards_original_position.append(card.position)
                    #     self.pull_to_top(card)
                # If it is the cpu's turn no cards should be moved from the player's hand
                elif not self.player_turn and pile_index not in range(C.PLAY_PILE_1, C.PLAY_PILE_7+1):
                    # All other cases, grab the face-up card we are clicking on
                    self.held_cards = [primary_card]
                    # Save the position
                    self.held_cards_original_position = [self.held_cards[0].position]
                    # Put on top in drawing order
                    self.pull_to_top(self.held_cards[0])

                    # For UNO only one card should be played at a time
                    # So we should only be able to move one card at a time
                    # # Is this a stack of cards? If so, grab the other cards too
                    # card_index = self.piles[pile_index].index(primary_card)
                    # for i in range(card_index + 1, len(self.piles[pile_index])):
                    #     card = self.piles[pile_index][i]
                    #     self.held_cards.append(card)
                    #     self.held_cards_original_position.append(card.position)
                    #     self.pull_to_top(card)

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == C.BOTTOM_FACE_DOWN_PILE and len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) == 0:
                    self.reuse_cards()

    def remove_card_from_pile(self, card, is_discarded=False):
        """ Remove card from whatever pile it was in. """
        index = 0
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                if 1 <= index <= 7:
                    self.player_hand.remove_card(card)
                elif index <= 14 and is_discarded:
                    # print("Remove cpu card:", card.colors, card.type, card.points)
                    # print("CPU Hand (before):", end=" ")
                    # for card2 in self.cpu_hand.cards:
                    #     print(card2.colors, card2.type, card2.points, end=", ")
                    # print()
                    self.cpu_hand.remove_card(card)
                    # print("CPU Hand (after):", end=" ")
                    # for card2 in self.cpu_hand.cards:
                    #     print(card2.colors, card2.type, card2.points, end=", ")
                    # print()

                break
            index += 1

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        move_to_discard = False

        if 1 <= pile_index <= 7:
            self.player_hand.add_card(card)
        elif pile_index == C.DISCARD_PILE:
            move_to_discard = True

            if card.type != "Skip" and card.type != "Reverse" and card.type != "Draw2" and card.type != "Draw4":
                print("Change Turn", card.type)
                self.player_turn = not self.player_turn

            if card.type == "Draw4":
                # Need to choose color + force draw 4 cards
                if len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) >= 4:
                    for i in range(4):
                        self.draw_card(not self.player_turn, True)
                else:
                    for i in range(len(self.piles[C.BOTTOM_FACE_DOWN_PILE])):
                        self.draw_card(not self.player_turn, True)
            elif card.type == "Draw2":
                # Force draw 2 cards
                if len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) >= 2:
                    for i in range(2):
                        self.draw_card(not self.player_turn, True)
                else:
                    for i in range(self.piles[C.BOTTOM_FACE_DOWN_PILE]):
                        self.draw_card(not self.player_turn, True)

        self.remove_card_from_pile(card, move_to_discard)
        self.piles[pile_index].append(card)

        if move_to_discard and len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) < 4:
            print("Draw Pile Less Than 4")
            self.reuse_cards()

        if not self.player_turn and pile_index == C.DISCARD_PILE:
            # Something not working when playing a card (still in hand - specifically draw4)
            deck = self.piles[C.BOTTOM_FACE_DOWN_PILE]
            face_up = self.piles[C.DISCARD_PILE][-1]
            while Game_Logic.is_playable(face_up, self.cpu_hand).amount < 1:
                self.draw_card(False)

            cpu_choice = Game_Logic.cpu_select(self.piles[C.DISCARD_PILE][-1], self.cpu_hand, deck[:])
            print("CPU Chose")
            print(cpu_choice[0].colors, cpu_choice[0].type, cpu_choice[0].points)
            # self.move_card_to_new_pile(cpu_choice[0], C.DISCARD_PILE)
            cpu_card = cpu_choice[0]
            cpu_visual_card = ""
            # if cpu_card in self.piles:
            #     for pile_card in self.piles:
            #         if pile_card == cpu_card:
            #             cpu_visual_card = pile_card
            #
            # self.move_to_discard(C.DISCARD_PILE, cpu_choice[0])

            for card in cpu_choice[1]:
                self.draw_card(False, True)

        # print("CPU's Hand:")
        # for cpu_card in self.cpu_hand.cards:
        #     print(cpu_card.colors, cpu_card.type, cpu_card.points, end=", ")
        # print()
        # print("Player's Hand:")
        # for player_card in self.player_hand.cards:
        #     print(player_card.colors, player_card.type, player_card.points, end=", ")
        # print()
        # print("Position:", card.position)
        # print()

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a bottom play pile?
            elif C.PLAY_PILE_1 <= pile_index <= C.PLAY_PILE_7 and self.player_turn:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - C.CARD_VERTICAL_OFFSET * (i + 1)
                else:
                    # Are there no cards in the bottom play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - C.CARD_VERTICAL_OFFSET * i

                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False

            # Release on top play pile? And only one card held?
            elif C.TOP_PILE_1 <= pile_index <= C.TOP_PILE_7 and len(self.held_cards) == 1 and not self.player_turn:
                # Move position of card to pile
                self.held_cards[0].position = pile.position
                # Move card to card list
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                reset_position = False

            # The following elif contains our own custom code
            elif pile_index == C.DISCARD_PILE: # Make it so a user can play their card in the face up pile
                reset_position = self.move_to_discard(pile_index, pile)

                # reset_position = False


        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def draw_card(self, player_hand=True, forced_draw=False):
        if player_hand:
            player_playable = Game_Logic.is_playable(self.piles[C.DISCARD_PILE][-1], self.player_hand)
        else:
            player_playable = Game_Logic.is_playable(self.piles[C.DISCARD_PILE][-1], self.cpu_hand)

        if player_playable.amount < 1 or forced_draw:
            reset_draw_pile = False
            if self.piles[C.BOTTOM_FACE_DOWN_PILE][-1] == self.piles[C.BOTTOM_FACE_DOWN_PILE][0]:
                reset_draw_pile = True
            # Get top card
            card = self.piles[C.BOTTOM_FACE_DOWN_PILE][-1]
            # Flip face up
            card.face_up()
            if player_hand:
                # Move card position to bottom-right face up pile
                card.position = self.pile_mat_list[C.PLAY_PILE_1].position  # Modified
            else:
                print("CPU Draw Card Position Changed")
                card.position = self.pile_mat_list[C.TOP_PILE_1].position
            # Remove card from face down pile
            self.piles[C.BOTTOM_FACE_DOWN_PILE].remove(card)
            # self.deck.remove_card(card)
            if player_hand:
                # Move card to face up list
                self.piles[C.PLAY_PILE_1].append(card)  # Modified
                # Add card to player's hand
                self.player_hand.add_card(card)
            else:
                # Move card to face up list
                self.piles[C.TOP_PILE_1].append(card)  # Modified
                # Add card to player's hand
                print("CPU actual Draw", card.colors, card.type, card.points)
                self.cpu_hand.add_card(card)

            # Put on top draw-order wise
            self.pull_to_top(card)

            if reset_draw_pile:
                self.reuse_cards()

    def reuse_cards(self):

        # Flip the deck back over so we can restart
        temp_list = self.piles[C.DISCARD_PILE].copy()  # Modified
        # print("Flip Length:", self.deck.amount)

        # Shuffle the cards
        for pos1 in range(len(temp_list) - 1):
            pos2 = random.randrange(len(temp_list) - 1)
            temp_val = temp_list[pos1]
            temp_list[pos1] = temp_list[pos2]
            temp_list[pos2] = temp_val

        for card in reversed(temp_list[:-1]):
            if card.type == "Wild" or card.type == "Draw4":
                card.colors = "Wild"
            card.face_down()
            self.piles[C.DISCARD_PILE].remove(card)  # Modified
            self.piles[C.BOTTOM_FACE_DOWN_PILE].append(card)
            # self.deck.add_card(card)
            card.position = self.pile_mat_list[C.BOTTOM_FACE_DOWN_PILE].position

        # print("New Flip Length:", self.deck.amount)

    def move_to_discard(self, pile_index, pile):
        play_card = Uno_Card.Hand()
        play_card.add_card(self.held_cards[0])
        print("Color Compare:", self.piles[C.DISCARD_PILE][-1].colors, self.held_cards[0].colors)
        playable = Game_Logic.is_playable(self.piles[C.DISCARD_PILE][-1], play_card)

        if len(playable.cards) > 0:
            # Move position of card to pile
            card = self.held_cards[0]
            if card.colors == "Wild":
                card.colors = input("Choose color: ")
            card.position = pile.position
            self.move_card_to_new_pile(card, pile_index)
            return False
        else:
            return True

def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
