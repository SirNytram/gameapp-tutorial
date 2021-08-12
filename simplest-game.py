from gameapp.win_gameapp import GameAudio, GameShapeRect
from gameapp import GameApp, GameSection, GameImage, kb

class MainSection(GameSection):
    def on_start(self):
        self.bg = GameShapeRect(self.gameapp.rect, line_width=0)
        self.dino = GameImage('dino.png', (100,400))
        self.jumping = False
        self.jump_count = 10

        self.cactus = GameImage('cactus.png', (500, 400))
        self.gameover = False
        self.gameoversound = GameAudio('dead.wav')
        
    def on_loop(self):
        if not self.gameover:
            if self.jumping:
                if self.jump_count >= -10:
                    self.dino.position.y -= (self.jump_count * abs(self.jump_count)) * 0.3
                    self.jump_count -= 1
                else:
                    self.jump_count = 10
                    self.jumping = False

            self.cactus.position.x -= 5
            if self.cactus.position.x < -10:
                self.cactus.position.x = 700

            if self.dino.rect.collides(self.cactus.rect):
                self.gameover = True
                self.gameoversound.play()



    def on_render(self):
        self.bg.render()
        self.dino.render()
        self.cactus.render()

    def on_key(self, is_down, key, mod):
        if is_down and key == kb.K_SPACE:
            self.jumping = True
   

game = GameApp()
game.sections['main'] = MainSection(game, True)
game.start()