import Uno_Card


def is_playable(face_up, player_hand):
    # Code to determine what cards are playable based on
    # an inputted hand - returns a hand of playable cards


def cpu_select(face_up, player_hand, deck):
    # Code to determine what card the cpu will play on
    # it's turn - returns a single card

    # playable_cards = is_playable(face_up, player_hand)
    playable_cards = Uno_Card.Hand()
    playable_cards.add_card(Uno_Card.Card("Wild", "Wild", 50))

    drawn_cards = []

    while playable_cards.amount == 0:
        card = deck.cards[-1]
        deck.remove_card(card)
        drawn_cards.append(card)
        player_hand.add_card(card)
        playable_cards = is_playable(face_up, player_hand)

    selected_cards = Uno_Card.Hand()

    if playable_cards.amount > 1:
        for card in playable_cards.cards:
            if card.points == playable_cards.maxPoints:
                selected_cards.add_card(card)
    else:
        selected_cards.add_card(playable_cards.cards[0])

    if selected_cards.amount > 1:
        temp_cards = []
        for card in selected_cards.cards:
            if card.type_value(2) == selected_cards.maxType:
                temp_cards.append(card)

        selected_cards.cards = temp_cards

    if selected_cards.amount > 1:
        temp_cards = []
        for card in selected_cards.cards:
            if card.colors == "Red" and player_hand.red == player_hand.get_max_color():
                temp_cards.append(card)
            elif card.colors == "Green" and player_hand.green == player_hand.get_max_color():
                temp_cards.append(card)
            elif card.colors == "Blue" and player_hand.blue == player_hand.get_max_color():
                temp_cards.append(card)
            elif card.colors == "Yellow" and player_hand.yellow == player_hand.get_max_color():
                temp_cards.append(card)
            elif card.colors == "Wild":
                temp_cards.append(card)

        if len(temp_cards) == 0:
            for card in selected_cards.cards:
                if card.colors == "Red" and selected_cards.red == selected_cards.get_max_color():
                    temp_cards.append(card)
                elif card.colors == "Green" and selected_cards.green == selected_cards.get_max_color():
                    temp_cards.append(card)
                elif card.colors == "Blue" and selected_cards.blue == selected_cards.get_max_color():
                    temp_cards.append(card)
                elif card.colors == "Yellow" and selected_cards.yellow == selected_cards.get_max_color():
                    temp_cards.append(card)
                elif card.colors == "Wild":
                    temp_cards.append(card)

        selected_cards.cards = temp_cards

    return selected_cards.cards[0], drawn_cards
