from gameapp import GameApp, GameSection, GameImage, kb

class GameScreen(GameSection):
    def on_start(self):
        self.canon = GameImage('canon.png', self.gameapp.rect.midbottom).rotate(-90)

    def on_loop(self):
        if kb.K_RIGHT in self.gameapp.pressed_keys:
            self.canon.rotation -= 2

        if kb.K_LEFT in self.gameapp.pressed_keys:
            self.canon.rotation += 2

        self.canon.rotation = self.canon.get_angle_towards(game.mouse_position)

    def on_render(self):
        self.canon.render()

game = GameApp()
game.sections['main'] = GameScreen(game, True)
game.start() 