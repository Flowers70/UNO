import Mouse_Actions
import Constants as C
import Game_Logic
import Uno_Card


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
            cpu_card = cpu_choice[0]

            for card in cpu_choice[1]:
                self.draw_card(False, True)

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

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
