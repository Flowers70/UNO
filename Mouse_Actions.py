from typing import Optional

import arcade
import arcade.gui
import Uno_Card
import Constants as C
import random
import Game_Logic

import threading


# Changed arcade.Window -> arcade.View
class MouseActions(arcade.View):

    def __init__(self):
        # Removed: C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE
        super().__init__()

        # NEW CODE (Dec. 7)
        self.background = None
        self.color_chosen = threading.Event()
        self.uno_button_pressed = False  # has player pushed the uno button before going out?
        # Create the buttons from https://api.arcade.academy/en/latest/examples/gui_flat_button.html
        # UNO Button
        self.uno_manager = arcade.gui.UIManager()
        self.uno_manager.enable()
        uno_style = {
            "font_name": "copperplate",
            "font_size": 20,
            "font_color": arcade.color.AMBER,  # yellow
            "border_width": 0,
            "border_color": "none",
            "bg_color": (227, 38, 54),

            # used if button is pressed
            "bg_color_pressed": arcade.color.BLACK,
            # "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.WHITE,
        }

        # UNO Button
        self.uno_box = arcade.gui.UIBoxLayout()
        UNO_button = arcade.gui.UIFlatButton(text="UNO!", width=100, style=uno_style)
        self.uno_box.add(UNO_button.with_space_around(bottom=20))
        UNO_button.on_click = self.on_click_UNO
        self.uno_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="bottom",
                child=self.uno_box)
        )
        self.wild_right_manager = arcade.gui.UIManager()
        self.wild_right_manager.enable()
        self.wild_left_manager = arcade.gui.UIManager()
        self.wild_left_manager.enable()
        wild_green_style = {
            "font_name": "copperplate",
            "font_size": 25,
            "font_color": arcade.color.WHITE,
            "border_width": 0,
            "border_color": "none",
            "bg_color": (39, 174, 73),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            # "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        wild_red_style = {
            "font_name": "copperplate",
            "font_size": 25,
            "font_color": arcade.color.WHITE,
            "border_width": 0,
            "border_color": "none",
            "bg_color": (250, 88, 83),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            # "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        wild_yellow_style = {
            "font_name": "copperplate",
            "font_size": 25,
            "font_color": arcade.color.WHITE,
            "border_width": 0,
            "border_color": "none",
            "bg_color": (253, 170, 0),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            # "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        wild_blue_style = {
            "font_name": "copperplate",
            "font_size": 25,
            "font_color": arcade.color.WHITE,
            "border_width": 0,
            "border_color": "none",
            "bg_color": (83, 86, 250),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            # "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        self.wild_left_box = arcade.gui.UIBoxLayout()
        self.wild_right_box = arcade.gui.UIBoxLayout()
        wild_green_button = arcade.gui.UIFlatButton(text="Green", width=200, height=100, style=wild_green_style)
        wild_red_button = arcade.gui.UIFlatButton(text="Red", width=200, height=100, style=wild_red_style)
        wild_yellow_button = arcade.gui.UIFlatButton(text="Yellow", width=200, height=100, style=wild_yellow_style)
        wild_blue_button = arcade.gui.UIFlatButton(text="Blue", width=200, height=100, style=wild_blue_style)
        self.wild_left_box.add(wild_green_button.with_space_around(bottom=20))
        self.wild_left_box.add(wild_red_button.with_space_around(bottom=20))
        self.wild_right_box.add(wild_yellow_button.with_space_around(bottom=20))
        self.wild_right_box.add(wild_blue_button.with_space_around(bottom=20))
        wild_green_button.on_click = self.on_click_wild_green
        wild_red_button.on_click = self.on_click_wild_red
        wild_yellow_button.on_click = self.on_click_wild_yellow
        wild_blue_button.on_click = self.on_click_wild_blue
        self.wild_right_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="center_y",
                child=self.wild_right_box)
        )
        self.wild_left_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="center_y",
                child=self.wild_left_box)
        )

        # -------------------------

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

    # NEW CODE (Dec. 7)
    def on_click_wild_green(self, event):
        print("green BUTTON:")
        temp_list = self.piles[C.DISCARD_PILE].copy()
        print(temp_list[-1].colors)
        if temp_list[-1].colors == "Wild":
            temp_list[-1].colors = "Green"
        print(temp_list[-1].colors)
        # self.wild_left_manager.clear()
        # self.wild_right_manager.clear()
        self.color_chosen.set()

    def on_click_wild_red(self, event):
        print("red BUTTON")
        temp_list = self.piles[C.DISCARD_PILE].copy()
        print(temp_list[-1].colors)
        if temp_list[-1].colors == "Wild":
            temp_list[-1].colors = "Red"
        print(temp_list[-1].colors)
        # self.wild_left_manager.clear()
        # self.wild_right_manager.clear()
        self.color_chosen.set()


    def on_click_wild_yellow(self, event):
        print("yellow BUTTON")
        temp_list = self.piles[C.DISCARD_PILE].copy()
        print(temp_list[-1].colors)
        if temp_list[-1].colors == "Wild":
            temp_list[-1].colors = "Yellow"
        print(temp_list[-1].colors)
        # self.wild_left_manager.clear()
        # self.wild_right_manager.clear()
        self.color_chosen.set()

    def on_click_wild_blue(self, event):
        print("blue BUTTON")
        temp_list = self.piles[C.DISCARD_PILE].copy()
        print(temp_list[-1].colors)
        if temp_list[-1].colors == "Wild":
            temp_list[-1].colors = "Blue"
        print(temp_list[-1].colors)
        # self.wild_left_manager.clear()
        # self.wild_right_manager.clear()
        self.color_chosen.set()

    # UNO
    def on_click_UNO(self, event):
        print("UNO BUTTON:", self.player_hand.amount)
        if len(self.player_hand.cards) > 1:
            for i in range(2):
                self.draw_card(self.player_turn, True)
        elif len(self.player_hand.cards) == 1:
            self.uno_button_pressed = True

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
            print("Restart")
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
            if player_hand:
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
