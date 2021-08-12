from gameapp import GameApp, GameSection, kb, Rect, Point, Color, GameShapeCircle, GameShapeRect,GameText, GameShapeLine
import random

class MainSection(GameSection):
    def on_start(self):
        #create and initialize different game objects
        self.bg = GameShapeRect(self.gameapp.rect, line_width=0)
        self.border = GameShapeRect((50,50, 200, 500), Color('blue'))
        self.ball = GameShapeCircle(radius = 5, color = (255,0,0))
        self.reset_ball()
        self.basket = GameShapeRect((100,500, 20, 20), Color('red'))
        self.score = 0
        self.score_text = GameText('', (100,10), Color('green'))
        self.floor = GameShapeLine((55,525), (245, 525), Color('white'))
       
    def reset_ball(self):
        #reset the ball position on top of screen
        self.ball.position.y = 100
        self.ball.position.x = random.randint(100,200)

    def on_loop(self):
        #move ball down
        self.ball.position.y += 5

        #check if basket is moving
        if kb.K_RIGHT in self.gameapp.pressedKeys:
            self.basket.position.x += 2
        if kb.K_LEFT in self.gameapp.pressedKeys:
            self.basket.position.x -= 2

        #check if basket collides with ball
        if self.basket.rect.collides(self.ball.position):
            self.score += 1
            self.reset_ball()

        #check if ball is lower than basket 
        if self.ball.position.y > 530:
            self.score -= 1
            self.reset_ball()

    def on_render(self):
        #render all our objects
        self.bg.render()
        self.ball.render()
        self.basket.render()
        self.score_text.renderText(f'Score: {self.score}')
        self.border.render()
        self.floor.render()

    def on_key(self, isDown, key, mod):
        #if user press R, reset everything
        if isDown and key == kb.K_r:
            self.reset_ball()
            self.score = 0

#main code
game = GameApp(display_number = 1, height = 600, width=300)
game.sections['main'] = MainSection(game, True)
game.start()