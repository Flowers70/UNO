import arcade

import Mouse_Actions
import Constants as C
import Game_Logic
import Uno_Card
import GameOver
import time


class PileActions(Mouse_Actions.MouseActions):
    def remove_card_from_pile(self, card, is_discarded=False):
        """ Remove card from whatever pile it was in. """
        index = 0
        for pile in self.piles:
            if card in pile:
                pile.remove(card)

                if 1 <= index <= 7:
                    self.player_hand.remove_card(card)
                elif index <= 14 and is_discarded:
                    self.cpu_hand.remove_card(card)
                break
            index += 1

    def move_card_to_new_pile(self, card, pile_index, cpu_continuous_plays=0):
        """ Move the card to a new pile """
        move_to_discard = False

        if 1 <= pile_index <= 7:
            self.player_hand.add_card(card)
        elif pile_index == C.DISCARD_PILE:
            move_to_discard = True

            if card.type != "Skip" and card.type != "Reverse" and card.type != "Draw2" and card.type != "Draw4":
                self.player_turn = not self.player_turn
                cpu_continuous_plays = 0
                print("CPU Continuous plays 0")
            elif not self.player_turn:
                cpu_continuous_plays += 1
                print("CPU Continuous plays +1 ("+str(cpu_continuous_plays)+")")

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

        if len(self.cpu_hand.cards) == 0:
            print("GAME OVER!")
            view = GameOver.GameOverView(False)
            self.window.show_view(view)
        elif len(self.player_hand.cards) == 0:
            print("GAME OVER!")
            view = GameOver.GameOverView(True)
            self.window.show_view(view)

        if move_to_discard and len(self.piles[C.BOTTOM_FACE_DOWN_PILE]) < 4:
            print("Draw Pile Less Than 4")
            self.reuse_cards()

        if not self.player_turn and pile_index == C.DISCARD_PILE:
            self.cpu_play(cpu_continuous_plays)
            return cpu_continuous_plays
        else:
            return 0


    def move_to_discard(self, pile_index, pile):
        play_card = Uno_Card.Hand()
        play_card.add_card(self.held_cards[0])
        playable = Game_Logic.is_playable(self.piles[C.DISCARD_PILE][-1], play_card)
        self.piles[C.DISCARD_PILE][-1].face_up()

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

    def cpu_play(self, cpu_continuous_plays):
        deck = self.piles[C.BOTTOM_FACE_DOWN_PILE]
        face_up = self.piles[C.DISCARD_PILE][-1]
        while Game_Logic.is_playable(face_up, self.cpu_hand).amount < 1:
            self.draw_card(False)

        cpu_choice = Game_Logic.cpu_select(self.piles[C.DISCARD_PILE][-1], self.cpu_hand, deck[:])
        cpu_card = cpu_choice[0]

        for card in cpu_choice[1]:
            self.draw_card(False, True)

        cpu_wild = False

        # Determining a color when card is a wild
        if cpu_card.colors == "Wild":
            cpu_wild = True
            if self.cpu_hand.red == self.cpu_hand.get_max_color():
                cpu_card.colors = "Red"
            elif self.cpu_hand.green == self.cpu_hand.get_max_color():
                cpu_card.colors = "Green"
            elif self.cpu_hand.blue == self.cpu_hand.get_max_color():
                cpu_card.colors = "Blue"
            else:
                cpu_card.colors = "Yellow"

        print("CPU Playing:", cpu_card.colors, cpu_card.type, cpu_card.points)
        # Implementing logic so CPU automatically plays the card selected
        pile_index_cpu_choice = self.get_pile_for_card(cpu_card)

        cpu_pile = self.piles[pile_index_cpu_choice]
        index_of_card = 0
        for i in range(len(cpu_pile)):
            if (cpu_wild and cpu_pile[i].colors == "Wild" or cpu_pile[i].colors == cpu_card.colors
            and cpu_pile[i].type == cpu_card.type and cpu_pile[i].points == cpu_card.points):
                index_of_card = i

        cpu_card_position = self.pile_mat_list[pile_index_cpu_choice].position
        cards = arcade.get_sprites_at_point(cpu_card_position, self.card_list)
        cards[index_of_card].position = (358.8, 290.625)
        self.pull_to_top(cards[index_of_card])
        turns = 0
        turns += self.move_card_to_new_pile(cards[index_of_card], C.DISCARD_PILE, cpu_continuous_plays)
        print("Num Plays Continuous:", cpu_continuous_plays)
        index = cpu_continuous_plays * -1 - 1
        current_face_up_card = self.piles[C.DISCARD_PILE][index]
        print("Discard Pile:", end=" ")
        for card in self.piles[C.DISCARD_PILE]:
            print(card.colors, card.type, card.points, end=", ")
        print()
        print("Discard Pile (flip):", current_face_up_card.colors, current_face_up_card.type, current_face_up_card.points)
        current_face_up_card.face_up()
        print("Turns:", turns)

        # if cpu_continuous_plays > 0:
        #     print("Sleep")
        #     time.sleep(3)

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
