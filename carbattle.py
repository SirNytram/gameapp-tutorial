from pygame.draw import line
from gameapp import GameApp, GameSection, GameImage, kb, GameAudio, GameText, GameFont, Rect, Point, Color, GameTimer, GameShapeRect, GameShapeCircle
from typing import List
from random import randint

class CarLevel(GameSection):
    def on_start(self):
        self.bg = GameShapeRect(self.gameapp.rect, color=Color('black'), line_width=0)
        # self.car_boundaries = GameShapeRect(color=Color('green'))
        self.crash_boundaries = GameShapeCircle(radius=20, color=Color('green'))
        self.player_car = GameImage('car_red.png', (200,200), scale=0.5, show_rect=True)
        self.enemy_car = GameImage('car_red.png', (400,200), scale=0.5)
        self.player_car.rotate(90)
        self.enemy_car.rotate(90)
        self.crash_sound = GameAudio('crash.wav')
        self.bg_music = GameAudio('background.wav')
        # self.bg_music.play(-1)
        self.text = GameText('', (0,0), (255,0,0), anchor_point=(0,0))
        self.coin = GameShapeCircle( (randint(0, int(self.gameapp.rect.right)), randint(0, int(self.gameapp.rect.bottom))) , 
                        radius=4, 
                        color=Color('yellow'), 
                        line_width=0)
        self.gameapp.addTimer('flappy', 100)
        self.iscolliding = False
        self.auto_follow = False
        self.player_bullets:List[GameShapeCircle] = []


    def on_loop(self):
        if kb.K_UP in self.gameapp.pressedKeys:
            if not self.iscolliding:
                self.player_car.moveAngle(10, self.player_car.rotation)

        if kb.K_DOWN in self.gameapp.pressedKeys:
            self.player_car.moveAngle(-10, self.player_car.rotation)


        if kb.K_RIGHT in self.gameapp.pressedKeys:
            self.player_car.rotation -= 5

        if kb.K_LEFT in self.gameapp.pressedKeys:
            self.player_car.rotation += 5


        if self.player_car.position.distanceTo(self.enemy_car.position) < 40:
            if not self.iscolliding:
                self.crash_sound.play()
            self.iscolliding = True
        else:
            self.iscolliding = False 

        for bullet in self.player_bullets:
            bullet.moveAngle(5, bullet.rotation)
            if bullet.position.x < 0 or bullet.position.y < 0 or bullet.position.x > self.gameapp.rect.right or bullet.position.y > self.gameapp.rect.bottom:
                self.player_bullets.remove(bullet)

        if self.auto_follow:
            self.enemy_car.moveTo(5, self.player_car.position)

    def on_render(self):
        self.bg.render()
        for bullet in self.player_bullets:
            bullet.render()

        self.player_car.render()
        self.enemy_car.render()
        # self.text.renderText(f'L {self.player_car.rect.left:.0f} T {self.player_car.rect.top:.0f}  R {self.player_car.rect.right:.0f}  B {self.player_car.rect.bottom:.0f}')
        self.coin.render()

        # self.car_boundaries.rect = self.player_car.rect.copy()  #setrect
        # self.car_boundaries.render()
        self.crash_boundaries.position = self.player_car.position
        self.crash_boundaries.render()
        

    def on_key(self, is_down, key, mod):
        if is_down:
            if key == kb.K_a:
                self.auto_follow = not self.auto_follow

            if key == kb.K_RCTRL:
                bullet = GameShapeCircle(center=self.player_car.position, radius=4,color=Color('red'), line_width=0)
                bullet.rotation = self.player_car.rotation
                self.player_bullets.append(bullet)

            if key == kb.K_ESCAPE:
                self.gameapp.quit()


game = GameApp(display_number=1, width= 600, height=600)
game.sections['car'] = CarLevel(game, True)
game.start()