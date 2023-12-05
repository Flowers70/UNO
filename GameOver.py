import arcade
import Constants as C

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, player_won):
        """ This is run once when we switch to this view """
        super().__init__()

        if player_won:
            image = "venv/lib/you_won_gameover.png"
        else:
            image = "venv/lib/cpu_won_gameover.png"

        self.texture = arcade.load_texture(image)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, C.SCREEN_WIDTH - 1, 0, C.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_sized(C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2,
                                C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    # def on_mouse_press(self, _x, _y, _button, _modifiers):
    #     """ If the user presses the mouse button, re-start the game. """
    #     game_view = main.MyGameView()
    #     game_view.setup()
    #     self.window.show_view(game_view)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            print("Restart 2")
            from main import MyGameView
            game_view = MyGameView()
            game_view.setup()
