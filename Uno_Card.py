import Constants as C
import arcade


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, colors, type, points, scale=0.7):
        """ Card constructor """

        # Attributes for colors and value
        self.colors = colors
        self.type = type
        self.points = points

        # Image to use for the sprite when face up
        #self.image_file_name = f":resources:images/cards/card{self.colors}{self.value}.png"
        value = ""
        if self.type == "Normal":
            value = self.points
        else:
            value = self.type

        self.image_file_name = f"venv/Lib/Uno_cards/{self.colors}_{value}.png"
        self.is_face_up = False
        super().__init__(C.FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(C.FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    def type_value(self, num_of_players):
        if self.points < 10:
            return 1
        elif self.type == "Wild":
            return 2
        elif self.type == "Draw4":
            return 3
        elif num_of_players == 2:
            if self.type == "Draw2":
                return 2
            else:
                return 3
        else:
            if self.type == "Draw2":
                return 3
            else:
                return 2

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up


def create_every_card(storage_list):  # We created this
    draw_pile = C.START_X + 4 * C.X_SPACING, C.MIDDLE_Y

    for card_color in C.CARD_COLORS:
        for card_type_num in range(1, 3):
            for card_type in C.CARD_TYPES[card_type_num]:

                if card_type_num == 1:
                    point_value = 20
                    card = Card(card_color, card_type, point_value)
                    card.position = draw_pile
                    storage_list.append(card)

                    card2 = Card(card_color, card_type, point_value)
                    card2.position = draw_pile
                    storage_list.append(card2)
                else:
                    zero_card = Card(card_color, card_type, 0)
                    zero_card.position = draw_pile
                    storage_list.append(zero_card)
                    for i in range(1, 9):
                        card = Card(card_color, card_type, i)
                        card.position = draw_pile
                        storage_list.append(card)

                        card2 = Card(card_color, card_type, i)
                        card2.position = draw_pile
                        storage_list.append(card2)

    for i in range(4):
        card = Card("Wild", "Wild", 50)
        card2 = Card("Wild", "Draw4", 50)
        card.position = draw_pile
        card2.position = draw_pile
        storage_list.append(card)
        storage_list.append(card2)


class Hand():
    def __init__(self):
        self.cards = list()
        self.amount = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.yellow = 0
        self.maxPoints = 0
        self.maxType = 0

    def add_card(self, card):
        self.cards.append(card)
        self.amount += 1

        if card.points > self.maxPoints:
            self.maxPoints = card.points

        if card.type_value(2) > self.maxType:
            self.maxType = card.type_value(2)

        if card.colors == "Red":
            self.red += 1
        elif card.colors == "Green":
            self.green += 1
        elif card.colors == "Blue":
            self.blue += 1
        elif card.colors == "Yellow":
            self.yellow += 1

    def remove_card(self, card):
        card_found = False

        for hand_card in range(len(self.cards)):
            if (self.cards[hand_card].colors == card.colors and
            self.cards[hand_card].type == card.type and
            self.cards[hand_card].points == card.points):
                card_found = True
                del self.cards[hand_card]

                if card.points == self.maxPoints:
                    self.maxPoints = 0
                    for card_self in self.cards:
                        if card_self.points > self.maxPoints:
                            self.maxPoints = card_self.points

                if card.type_value(2) == self.maxType:
                    self.maxType = 0
                    for card_self in self.cards:
                        if card_self.type_value(2) > self.maxType:
                            self.maxType = card_self.type_value(2)

                if card.colors == "Red":
                    self.red -= 1
                elif card.colors == "Green":
                    self.green -= 1
                elif card.colors == "Blue":
                    self.blue -= 1
                elif card.colors == "Yellow":
                    self.yellow -= 1

                break
        if not card_found:
            print("Card never found")

    def card_amount(self):
        return self.amount

    def get_max_color(self):
        max_value = max(self.red, self.blue, self.yellow, self.green)
        return max_value
