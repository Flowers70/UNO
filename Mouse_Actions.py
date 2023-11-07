from typing import Optional

import arcade
import Uno_Card
import Constants as C
import random
import Game_Logic


class MouseActions(arcade.Window):

    def __init__(self):
        super().__init__(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None
        self.player_turn = True
        # List of cards we are dragging with the mouse
        self.held_cards = None
        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None
        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None
        # Create a list of lists, each holds a pile of cards.
        self.piles = None
        # CPU hand (contains all cards in cpu's hand)
        self.cpu_hand = Uno_Card.Hand()

        # Players' hand (contains all cards in player's hand)
        self.player_hand = Uno_Card.Hand()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

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
                primary_card.face_up()
            elif pile_index != C.DISCARD_PILE:
                # Determine if it is the cpu's turn or the players
                # If it is the player's turn no cards should be moved from the cpu's hand
                if self.player_turn and pile_index not in range(C.TOP_PILE_1, C.TOP_PILE_7 + 1):
                    # All other cases, grab the face-up card we are clicking on
                    self.held_cards = [primary_card]
                    # Save the position
                    self.held_cards_original_position = [self.held_cards[0].position]
                    # Put on top in drawing order
                    self.pull_to_top(self.held_cards[0])
                # If it is the cpu's turn no cards should be moved from the player's hand
                elif not self.player_turn and pile_index not in range(C.PLAY_PILE_1, C.PLAY_PILE_7 + 1):
                    # All other cases, grab the face-up card we are clicking on
                    self.held_cards = [primary_card]
                    # Save the position
                    self.held_cards_original_position = [self.held_cards[0].position]
                    # Put on top in drawing order
                    self.pull_to_top(self.held_cards[0])

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == C.BOTTOM_FACE_DOWN_PILE and len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) == 0:
                    self.reuse_cards()

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
            elif pile_index == C.DISCARD_PILE:  # Make it so a user can play their card in the face up pile
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

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()

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
